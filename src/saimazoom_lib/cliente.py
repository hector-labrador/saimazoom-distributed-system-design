# cliente.py
# -*- coding: utf-8 -*-

"""
cliente.py
----------
Define la clase Cliente, que representa a un usuario registrado en el sistema Saimazoom.

"""

class Cliente:
    """
    Clase Cliente
    ------------
    Representa a un cliente de Saimazoom, con un identificador único
    y, potencialmente, otros datos como contraseña, dirección, etc.
    """

    def __init__(self, nombre_usuario: str, contrasenia: str = ""):
        """
        :param nombre_usuario: Identificador único del cliente .
        :param contrasenia: Contraseña del cliente.
        """
        self.nombre_usuario = nombre_usuario
        self.contrasenia = contrasenia

    def __str__(self):
        return f"Cliente({self.nombre_usuario})"

    def validar_credenciales(self, nombre_ingresado: str, contrasenia_ingresada: str) -> bool:
        """
        Verifica si las credenciales dadas coinciden con las del cliente.
        """
        return (self.nombre_usuario == nombre_ingresado 
                and self.contrasenia == contrasenia_ingresada)
