# messaging.py
# -*- coding: utf-8 -*-

"""
messaging.py
------------
Provee funciones y clases de utilidad para la conexión a RabbitMQ, 
la declaración de colas, etc.
"""

import pika
import logging

ROBOT_QUEUE = "2323-09_robot_queue"
REPARTIDOR_QUEUE = "2323-09_repartidor_queue"
ROBOT_TO_CONTROLLER_QUEUE = "2323-09_robot_responses"
REPARTIDOR_TO_CONTROLLER_QUEUE = "2323-09_repartidor_responses"


class RabbitMQConfig:
    def __init__(self, host="localhost", port=5672, username="guest", password="guest"):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def get_connection_parameters(self):
        credentials = pika.PlainCredentials(self.username, self.password)
        return pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            credentials=credentials
        )

def declare_queues(channel, queue_names: list):
    for q_name in queue_names:
        channel.queue_declare(queue=q_name, durable=False, auto_delete=True)
        logging.debug(f"Declarada cola '{q_name}' (durable=False, auto_delete=True)")

def connect_and_declare(config: RabbitMQConfig, queues: list):
    connection = pika.BlockingConnection(config.get_connection_parameters())
    channel = connection.channel()
    declare_queues(channel, queues)
    return connection, channel
