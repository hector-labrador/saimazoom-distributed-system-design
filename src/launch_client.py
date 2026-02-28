#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
launch_client.py
----------------
Este script inicia un cliente que se conecta al sistema Saimazoom para 
realizar acciones como registrar un nuevo usuario, iniciar sesión, gestionar pedidos, etc.

"""


import sys
from saimazoom_lib.controller import Controller
from saimazoom_lib.cliente_cli import ClienteCLI


def main():
    print("Saimazoom Client is starting...")
    controller = Controller()
    cli = ClienteCLI(controller)
    cli.run_cli()

    print("Saimazoom Client has finished.")

if __name__ == "__main__":
    main()