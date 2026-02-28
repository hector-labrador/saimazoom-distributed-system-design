# controller.py
# -- coding: utf-8 --

"""
controller.py
-------------
Define la clase Controller, que gestionará la lógica central de Saimazoom:
 - Manejo de clientes (registro, login)
 - Gestión de pedidos (posteriormente)
 - Conexión con RabbitMQ (posteriormente)
 - Persistencia de datos en ficheros o base de datos
"""
import configparser
import json
import logging

from saimazoom_lib.messaging import (
    RabbitMQConfig, connect_and_declare,
    ROBOT_QUEUE, REPARTIDOR_QUEUE,
    ROBOT_TO_CONTROLLER_QUEUE, REPARTIDOR_TO_CONTROLLER_QUEUE
)
from saimazoom_lib.sqldatabase import (
    create_table_clients, insert_client, find_client,
    create_table_orders, insert_order, get_orders_by_client,
    update_order_status, get_order_status
)

ESTADO_SOLICITADO = "Solicitado"
ESTADO_EN_ALMACEN = "En_Almacen"
ESTADO_EN_CINTA = "En_Cinta"
ESTADO_EN_REPARTO = "En_Reparto"
ESTADO_ENTREGADO = "Entregado"
ESTADO_CANCELADO = "Cancelado"

class Controller:
    def __init__(self, config_file="config/server.conf"):
        self.config_file = config_file
        self.is_running = False
        self.connection = None
        self.channel = None

        config = configparser.ConfigParser()
        config.read(self.config_file)
        log_level_str = config.get("Logging", "level", fallback="INFO")
        numeric_level = getattr(logging, log_level_str.upper(), logging.INFO)
        logging.basicConfig(level=numeric_level, format='[%(levelname)s] %(message)s')

        create_table_clients()
        create_table_orders()

        host = config.get("RabbitMQ", "host", fallback="localhost")
        port = config.getint("RabbitMQ", "port", fallback=5672)
        user = config.get("RabbitMQ", "username", fallback="guest")
        pwd = config.get("RabbitMQ", "password", fallback="guest")

        self.rabbit_config = RabbitMQConfig(host, port, user, pwd)
        logging.info(f"Controller iniciado con config_file={self.config_file}")

    def run(self):
        self.is_running = True
        queues = [
            ROBOT_QUEUE, REPARTIDOR_QUEUE,
            ROBOT_TO_CONTROLLER_QUEUE, REPARTIDOR_TO_CONTROLLER_QUEUE
        ]
        self.connection, self.channel = connect_and_declare(self.rabbit_config, queues)
        logging.info("Controller en ejecución y colas declaradas.")

        # Consumimos Robot->Controller y Repartidor->Controller en el mismo hilo:
        self.channel.basic_consume(
            queue=ROBOT_TO_CONTROLLER_QUEUE,
            on_message_callback=self.on_robot_response,
            auto_ack=True
        )
        self.channel.basic_consume(
            queue=REPARTIDOR_TO_CONTROLLER_QUEUE,
            on_message_callback=self.on_repartidor_response,
            auto_ack=True
        )
        logging.info("Controller consumiendo Robot->Controller y Repartidor->Controller en un único start_consuming.")

        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            logging.warning("Controller interrumpido con Ctrl+C.")
        except Exception as e:
            logging.error(f"Error global en start_consuming: {e}")

    def stop(self):
        self.is_running = False
        if self.connection and not self.connection.is_closed:
            self.connection.close()
            logging.info("Conexión RabbitMQ cerrada.")
        logging.info("Controller detenido.")


    def on_robot_response(self, ch, method, props, body):
        msg = json.loads(body.decode())
        accion = msg.get("accion", "")
        if accion == "PRODUCT_MOVED":
            pedido_id = msg.get("pedido_id", "??")
            prods_fail = msg.get("productos_no_encontrados", [])
            if prods_fail:
                logging.info(f"Robot informa que faltan {len(prods_fail)} productos en pedido {pedido_id}. No avanzamos a 'En_Cinta'.")
            else:
                logging.info(f"Todos los productos de pedido {pedido_id} OK. Avanzamos a 'En_Cinta'.")
                self.progress_order_state(pedido_id, ESTADO_EN_CINTA)
        else:
            logging.warning(f"Mensaje desconocido Robot->Controller: {msg}")

    def on_repartidor_response(self, ch, method, props, body):
        msg = json.loads(body.decode())
        accion = msg.get("accion", "")
        if accion == "PRODUCT_DELIVERED":
            pedido_id = msg.get("pedido_id", "??")
            entregado = msg.get("entregado", False)
            intentos = msg.get("intentos_usados", 0)
            if entregado:
                logging.info(f"Repartidor: Pedido {pedido_id} ENTREGADO con éxito en {intentos} intentos.")
                self.progress_order_state(pedido_id, ESTADO_ENTREGADO)
            else:
                logging.info(f"Repartidor: Pedido {pedido_id} NO ENTREGADO tras {intentos} intentos.")
        else:
            logging.warning(f"Mensaje desconocido Repartidor->Controller: {msg}")

    def register_client(self, nombre_usuario, contrasenia):
        res = insert_client(nombre_usuario, contrasenia)
        if res:
            logging.info(f"Cliente '{nombre_usuario}' registrado.")
        else:
            logging.warning(f"Error o duplicado al registrar cliente '{nombre_usuario}'.")
        return res

    def login_client(self, nombre_usuario, contrasenia):
        found = find_client(nombre_usuario, contrasenia)
        if found:
            logging.info(f"Cliente '{nombre_usuario}' inició sesión.")
        else:
            logging.warning(f"Fallo de credenciales para '{nombre_usuario}'.")
        return found

    def place_order(self, order_id, cliente_id, productos):
        ok = insert_order(order_id, cliente_id, productos, ESTADO_SOLICITADO)
        if ok:
            logging.info(f"Pedido '{order_id}' creado para '{cliente_id}'.")
        else:
            logging.warning(f"Error al crear pedido '{order_id}'.")
        return ok

    def get_client_orders(self, cliente_id):
        return get_orders_by_client(cliente_id)

    def cancel_order(self, order_id):
        curr = get_order_status(order_id)
        if curr is None:
            logging.warning(f"No existe el pedido '{order_id}'.")
            return False, "No existe el pedido."
        if curr in [ESTADO_ENTREGADO, ESTADO_CANCELADO, ESTADO_EN_REPARTO]:
            return False, f"No se puede cancelar en estado {curr}."
        updated = update_order_status(order_id, ESTADO_CANCELADO)
        if updated:
            logging.info(f"Pedido '{order_id}' cancelado.")
            return True, "Pedido cancelado"
        else:
            return False, "Error al cancelar."

    def progress_order_state(self, order_id, new_state):
        curr = get_order_status(order_id)
        if curr is None:
            return False
        valid = {
            ESTADO_SOLICITADO: [ESTADO_EN_ALMACEN, ESTADO_CANCELADO],
            ESTADO_EN_ALMACEN: [ESTADO_EN_CINTA, ESTADO_CANCELADO],
            ESTADO_EN_CINTA: [ESTADO_EN_REPARTO, ESTADO_CANCELADO],
            ESTADO_EN_REPARTO: [ESTADO_ENTREGADO, ESTADO_CANCELADO],
            ESTADO_ENTREGADO: [],
            ESTADO_CANCELADO: []
        }
        if new_state in valid.get(curr, []):
            ok = update_order_status(order_id, new_state)
            if ok:
                logging.info(f"Pedido '{order_id}' pasa de {curr} a {new_state}.")
            return ok
        else:
            logging.warning(f"Transición inválida: {curr} -> {new_state}")
            return False

    def send_to_robot(self, pedido_id, productos):
        if not self.channel:
            logging.error("No hay canal RabbitMQ")
            return
        self.progress_order_state(pedido_id, ESTADO_EN_ALMACEN)
        msg = {
            "accion": "MOVE_PRODUCT",
            "pedido_id": pedido_id,
            "productos": productos
        }
        self.channel.basic_publish(exchange='', routing_key=ROBOT_QUEUE, body=json.dumps(msg))
        logging.info(f"Enviado MOVE_PRODUCT de {pedido_id} al Robot.")

    def send_to_repartidor(self, pedido_id, direccion, productos):
        if not self.channel:
            logging.error("No hay canal RabbitMQ")
            return
        self.progress_order_state(pedido_id, ESTADO_EN_CINTA)
        self.progress_order_state(pedido_id, ESTADO_EN_REPARTO)
        msg = {
            "accion": "DELIVER_PRODUCT",
            "pedido_id": pedido_id,
            "direccion": direccion,
            "productos": productos
        }
        self.channel.basic_publish(exchange='', routing_key=REPARTIDOR_QUEUE, body=json.dumps(msg))
        logging.info(f"Enviado DELIVER_PRODUCT de {pedido_id} al Repartidor, dir={direccion}.")
