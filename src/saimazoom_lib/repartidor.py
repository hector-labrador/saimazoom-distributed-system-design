# repartidor.py
# -- coding: utf-8 --

"""
repartidor.py
-------------
Define la clase Repartidor, que simula el proceso de entregar productos 
al domicilio del cliente en Saimazoom.

"""
import time
import random
import logging
import json
import configparser
import pika

from saimazoom_lib.messaging import (
    RabbitMQConfig, declare_queues,
    REPARTIDOR_QUEUE, REPARTIDOR_TO_CONTROLLER_QUEUE
)

class Repartidor:
    def __init__(self, repartidor_id=1, max_intentos=3, prob_exito=0.7, config_file="config/server.conf"):
        """
        :param repartidor_id: ID del repartidor
        :param max_intentos: número máximo de intentos
        :param prob_exito: prob. de éxito en cada intento
        :param config_file: para leer host/puerto/cred. de RabbitMQ
        """
        self.repartidor_id = repartidor_id
        self.max_intentos = max_intentos
        self.prob_exito = prob_exito
        self.is_running = False

        parser = configparser.ConfigParser()
        parser.read(config_file)
        host = parser.get("RabbitMQ", "host", fallback="localhost")
        port = parser.getint("RabbitMQ", "port", fallback=5672)
        user = parser.get("RabbitMQ", "username", fallback="guest")
        pwd = parser.get("RabbitMQ", "password", fallback="guest")
        self.rabbit_config = RabbitMQConfig(host, port, user, pwd)

        logging.info(f"[Repartidor {self.repartidor_id}] Creado. max_intentos={max_intentos}, prob_exito={prob_exito}")

    def start(self):
        self.is_running = True
        logging.info(f"[Repartidor {self.repartidor_id}] Iniciando...")

    def stop(self):
        self.is_running = False
        logging.info(f"[Repartidor {self.repartidor_id}] Detenido.")

    def start_consuming(self):
        connection = pika.BlockingConnection(self.rabbit_config.get_connection_parameters())
        channel = connection.channel()

        declare_queues(channel, [REPARTIDOR_QUEUE, REPARTIDOR_TO_CONTROLLER_QUEUE])
        logging.info(f"[Repartidor {self.repartidor_id}] Escuchando '{REPARTIDOR_QUEUE}' y notificará a '{REPARTIDOR_TO_CONTROLLER_QUEUE}'")

        def callback(ch, method, properties, body):
            msg = json.loads(body.decode())
            accion = msg.get("accion", "")
            if accion == "DELIVER_PRODUCT":
                pedido_id = msg.get("pedido_id", "??")
                direccion = msg.get("direccion", "??")
                productos = msg.get("productos", [])
                logging.info(f"[Repartidor {self.repartidor_id}] Recibida orden DELIVER_PRODUCT (pedido {pedido_id}), {len(productos)} items.")
                self.simular_entrega(pedido_id, direccion, productos, channel)
            else:
                logging.warning(f"[Repartidor {self.repartidor_id}] Mensaje desconocido: {msg}")
            ch.basic_ack(delivery_tag=method.delivery_tag)

        channel.basic_consume(queue=REPARTIDOR_QUEUE, on_message_callback=callback, auto_ack=False)
        try:
            channel.start_consuming()
        except Exception as e:
            logging.error(f"[Repartidor {self.repartidor_id}] Error en consumo: {e}")
        finally:
            connection.close()

    def simular_entrega(self, pedido_id, direccion, productos, channel):
        """
        Intenta entregar con prob_exito por intento. Si lo logra, notifica "PRODUCT_DELIVERED" con entregado=True.
        Si falla en todos los intentos, entregado=False.
        """
        entregado = False
        for intento in range(1, self.max_intentos + 1):
            tiempo = random.randint(2, 4)
            logging.info(f"[Repartidor {self.repartidor_id}] Intento {intento} de entregar pedido {pedido_id} (espera {tiempo}s).")
            time.sleep(tiempo)
            if random.random() < self.prob_exito:
                logging.info(f"[Repartidor {self.repartidor_id}] Pedido {pedido_id} ENTREGADO en intento {intento}.")
                entregado = True
                self.publicar_resultado(pedido_id, True, intento, channel)
                return
            else:
                logging.info(f"[Repartidor {self.repartidor_id}] Fallo en intento {intento}.")

        logging.info(f"[Repartidor {self.repartidor_id}] Pedido {pedido_id} NO ENTREGADO tras {self.max_intentos} intentos.")
        self.publicar_resultado(pedido_id, False, self.max_intentos, channel)

    def publicar_resultado(self, pedido_id, entregado, intentos, channel):
        result = {
            "accion": "PRODUCT_DELIVERED",
            "pedido_id": pedido_id,
            "entregado": entregado,
            "intentos_usados": intentos
        }
        channel.basic_publish(
            exchange='',
            routing_key=REPARTIDOR_TO_CONTROLLER_QUEUE,
            body=json.dumps(result)
        )
        logging.info(f"[Repartidor {self.repartidor_id}] Notificado al Controller: PRODUCT_DELIVERED ({'exito' if entregado else 'fallo'}) en {intentos} intentos.")
