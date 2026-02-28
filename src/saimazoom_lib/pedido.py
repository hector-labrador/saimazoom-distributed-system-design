# pedido.py
# -*- coding: utf-8 -*-

"""
pedido.py
---------
Define la clase Pedido, que representa la solicitud de uno o varios productos
por parte de un cliente en el sistema Saimazoom.
"""

from enum import Enum

class EstadoPedido(Enum):
    """
    Enumeración estados de pedido
    """
    SOLICITADO = "Solicitado"
    EN_ALMACEN = "En_Almacen"
    EN_CINTA = "En_Cinta"
    EN_REPARTO = "En_Reparto"
    ENTREGADO = "Entregado"
    CANCELADO = "Cancelado"


class Pedido:
    """
    Clase Pedido
    -----------
    Representa un pedido en Saimazoom, asociado a un cliente. 
    Contendrá lista de productos, total, estado, etc.
    """

    def __init__(self, pedido_id: str, cliente_id: str, productos: list = None):
        """
        :param pedido_id: Identificador único del pedido.
        :param cliente_id: Identificador del cliente que realiza el pedido.
        :param productos: Lista de productos (IDs, dicts, u objetos) que componen el pedido.
        """
        self.pedido_id = pedido_id
        self.cliente_id = cliente_id
        self.productos = productos if productos is not None else []
        self.estado = EstadoPedido.SOLICITADO  # Por defecto, al crearse lo hemos puestp en SOLICITADO.

    def __str__(self):
        return (f"Pedido({self.pedido_id}) de Cliente({self.cliente_id}), "
                f"Estado: {self.estado.value}, "
                f"Productos: {len(self.productos)}")

    def cancelar(self):
        """
        Marca el pedido como CANCELADO, si su estado todavía lo permite.
        Aquí hemos pensado que podríamos validar si el pedido ya está en reparto o entregado.
        """
        if self.estado not in [EstadoPedido.ENTREGADO, EstadoPedido.CANCELADO]:
            self.estado = EstadoPedido.CANCELADO

    def avanzar_estado(self, nuevo_estado: EstadoPedido):
        """
        Actualiza el estado del pedido a 'nuevo_estado'.
        """
        self.estado = nuevo_estado