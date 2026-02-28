# robot.py
# -- coding: utf-8 --

"""
robot.py
--------
Define la clase Robot, que simula el proceso de mover productos 
del almacén a la cinta transportadora en Saimazoom.


"""
import time
import random
import logging
import json
import configparser
import pika

from saimazoom_lib.messaging import (
    RabbitMQConfig, declare_queues,
    ROBOT_QUEUE, ROBOT_TO_CONTROLLER_QUEUE
)

class Robot:
    def __init__(self, robot_id=1, prob_no_encontrar=0.1, config_file="config/server.conf"):
        """
        :param robot_id: Identificador del robot
        :param prob_no_encontrar: Probabilidad de NO encontrar un producto
        :param config_file: ruta a server.conf para leer el host de RabbitMQ
        """
        self.robot_id = robot_id
        self.prob_no_encontrar = prob_no_encontrar
        self.is_running = False

        parser = configparser.ConfigParser()
        parser.read(config_file)
        host = parser.get("RabbitMQ", "host", fallback="localhost")
        port = parser.getint("RabbitMQ", "port", fallback=5672)
        user = parser.get("RabbitMQ", "username", fallback="guest")
        pwd = parser.get("RabbitMQ", "password", fallback="guest")
        self.rabbit_config = RabbitMQConfig(host, port, user, pwd)

        logging.info(f"[Robot {robot_id}] Creado, config_file={config_file}, prob_no_encontrar={prob_no_encontrar}")

    def start(self):
        self.is_running = True
        logging.info(f"[Robot {self.robot_id}] Iniciando...")

    def stop(self):
        self.is_running = False
        logging.info(f"[Robot {self.robot_id}] Detenido.")

    def start_consuming(self):
        connection = pika.BlockingConnection(self.rabbit_config.get_connection_parameters())
        channel = connection.channel()

        declare_queues(channel, [ROBOT_QUEUE, ROBOT_TO_CONTROLLER_QUEUE])
        logging.info(f"[Robot {self.robot_id}] Escuchando '{ROBOT_QUEUE}' y notificará a '{ROBOT_TO_CONTROLLER_QUEUE}'")

        def callback(ch, method, properties, body):
            mensaje = json.loads(body.decode())
            accion = mensaje.get("accion", "")
            if accion == "MOVE_PRODUCT":
                pedido_id = mensaje.get("pedido_id", "??")
                productos = mensaje.get("productos", [])
                logging.info(f"[Robot {self.robot_id}] Orden MOVE_PRODUCT (pedido {pedido_id}), {len(productos)} items.")
                self.simular_mover_productos(pedido_id, productos, channel)
            else:
                logging.warning(f"[Robot {self.robot_id}] Mensaje desconocido: {mensaje}")
            ch.basic_ack(delivery_tag=method.delivery_tag)

        channel.basic_consume(queue=ROBOT_QUEUE, on_message_callback=callback, auto_ack=False)
        try:
            channel.start_consuming()
        except Exception as e:
            logging.error(f"[Robot {self.robot_id}] Error en consumo: {e}")
        finally:
            connection.close()

    def simular_mover_productos(self, pedido_id, productos, channel):
        prods_ok = []
        prods_fail = []
        for p in productos:
            pid = p.get("id", "???")
            if random.random() > self.prob_no_encontrar:
                self.mover_producto(pid)
                prods_ok.append(p)
            else:
                logging.info(f"[Robot {self.robot_id}] Producto '{pid}' NO encontrado.")
                prods_fail.append(p)

        result = {
            "accion": "PRODUCT_MOVED",
            "pedido_id": pedido_id,
            "productos_encontrados": prods_ok,
            "productos_no_encontrados": prods_fail
        }
        channel.basic_publish(exchange='', routing_key=ROBOT_TO_CONTROLLER_QUEUE, body=json.dumps(result))
        logging.info(f"[Robot {self.robot_id}] Notificado al Controller el resultado de pedido {pedido_id}.")

    def mover_producto(self, producto_id):
        logging.info(f"[Robot {self.robot_id}] Moviendo producto '{producto_id}' a la cinta...")
        tiempo = random.randint(2, 5)
        time.sleep(tiempo)
        logging.info(f"[Robot {self.robot_id}] Producto '{producto_id}' movido (tardó {tiempo}s).")
