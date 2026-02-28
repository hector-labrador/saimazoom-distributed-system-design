#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
commandline_client.py
---------------------
Script que lanza el cliente de línea de comandos (CLI) para interactuar con Saimazoom.

"""

import sys
from saimazoom_lib.controller import Controller
from saimazoom_lib.cliente_cli import ClienteCLI

def main():
    print("Saimazoom Client (commandline_client.py) is starting...")

    controller = Controller()
    controller.run()

    client_cli = ClienteCLI(controller)
    client_cli.run_cli()

    controller.stop()
    print("Saimazoom Client has finished.")

if __name__ == "__main__":
    main()
