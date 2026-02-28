#!/usr/bin/env python3
# -- coding: utf-8 --

"""
launch_controller.py
--------------------
Este script lanza el controlador principal de Saimazoom, 
que gestionará la lógica de pedidos, registro de clientes, etc.
"""

import sys
from saimazoom_lib.controller import Controller

def main():
    controller = Controller(config_file="config/server.conf")
    try:
        controller.run()
    except KeyboardInterrupt:
        logging.warning("Interrumpido con Ctrl+C.")
    finally:
        controller.stop()

if __name__ == "__main__":
    main()