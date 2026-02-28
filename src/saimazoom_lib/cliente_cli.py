# cliente_cli.py
# -*- coding: utf-8 -*-

"""
cliente_cli.py
--------------
Define la clase ClienteCLI, que gestiona las interacciones con un cliente a través
de la línea de comandos. Los métodos aquí definidos permitirán
enviar y recibir mensajes del Controller a través de RabbitMQ.
"""

class ClienteCLI:
    """
    Clase ClienteCLI:
    -----------------
    Maneja la interacción de un usuario-cliente con el sistema Saimazoom.
    Incluye métodos de registro, login, pedidos, etc.
    """

    def __init__(self, controller):
        """
        :param controller: Instancia del Controller
        """
        self.controller = controller
        self.username = None
        self.is_logged_in = False

    def run_cli(self):
        """
        Punto de entrada para interactuar con el usuario en consola.
        """
        print("[ClienteCLI] ¡Bienvenido a Saimazoom CLI!")
        while True:
            self._mostrar_menu_principal()
            opcion = input("Selecciona una opción: ").strip()
            if opcion == '1':
                self.registrar_cliente()
            elif opcion == '2':
                self.iniciar_sesion()
            elif opcion == '3':
                if self.is_logged_in:
                    self.realizar_pedido()
                else:
                    print("Debes iniciar sesión para realizar un pedido.")
            elif opcion == '4':
                if self.is_logged_in:
                    self.consultar_pedidos()
                else:
                    print("Debes iniciar sesión para consultar tus pedidos.")
            elif opcion == '5':
                if self.is_logged_in:
                    self.cancelar_pedido()
                else:
                    print("Debes iniciar sesión para cancelar un pedido.")
            elif opcion == '6':
                if self.is_logged_in:
                    self.enviar_a_robot()
                else:
                    print("Debes iniciar sesión primero.")
            elif opcion == '7':
                if self.is_logged_in:
                    self.enviar_a_repartidor()
                else:
                    print("Debes iniciar sesión primero.")
            elif opcion.lower() in ['q', 'quit', 'salir']:
                print("Saliendo de Saimazoom CLI...")
                break
            else:
                print("Opción no válida, inténtalo de nuevo.\n")

    def registrar_cliente(self):
        """
        Permite registrar un nuevo cliente en Saimazoom.
        """
        print("\n[Registrar Cliente]")
        if not self.controller:
            print("ERROR: No hay Controller configurado.")
            return
        nombre = input("Ingresa un nombre de usuario: ").strip()
        contrasenia = input("Ingresa una contraseña: ").strip()

        if not nombre or not contrasenia:
            print("El nombre o la contraseña no pueden estar vacíos.\n")
            return

        exito = self.controller.register_client(nombre, contrasenia)
        if exito:
            print(f"Cliente '{nombre}' registrado con éxito.\n")
        else:
            print(f"El nombre de usuario '{nombre}' ya existe o error al registrar.\n")

    def iniciar_sesion(self):
        """
        Permite iniciar sesión si el usuario está registrado.
        """
        print("\n[Iniciar Sesión]")
        if not self.controller:
            print("ERROR: No hay Controller configurado.")
            return

        nombre = input("Nombre de usuario: ").strip()
        contrasenia = input("Contraseña: ").strip()

        if not nombre or not contrasenia:
            print("Credenciales inválidas.\n")
            return

        exito = self.controller.login_client(nombre, contrasenia)
        if exito:
            self.username = nombre
            self.is_logged_in = True
            print(f"[ClienteCLI] Sesión iniciada como {self.username}\n")
        else:
            print("Error: Credenciales inválidas.\n")

    def realizar_pedido(self):
        print("\n[Realizar Pedido]")
        if not self.controller:
            print("ERROR: No hay Controller configurado.")
            return

        order_id = input("Ingresa un ID para tu pedido: ").strip()
        if not order_id:
            print("El ID de pedido no puede estar vacío.\n")
            return

        productos = []
        while True:
            prod_id = input("ID del producto (o dejar en blanco para terminar): ").strip()
            if not prod_id:
                break
            prod_name = input("Nombre del producto: ").strip()
            if not prod_name:
                print("El nombre del producto no puede ser vacío.")
                continue
            try:
                precio = float(input("Precio del producto: ").strip())
            except ValueError:
                print("Precio inválido. Inténtalo de nuevo.")
                continue

            productos.append({"id": prod_id, "nombre": prod_name, "precio": precio})

        if not productos:
            print("No se agregó ningún producto. Pedido abortado.\n")
            return

        ok = self.controller.place_order(order_id, self.username, productos)
        if ok:
            print(f"Pedido {order_id} creado y almacenado.\n")
        else:
            print(f"Error al crear el pedido {order_id} (posible duplicado o cliente inexistente).\n")

    def consultar_pedidos(self):
        print("\n[Consultar Pedidos]")
        if not self.controller:
            print("ERROR: No hay Controller configurado.")
            return

        pedidos = self.controller.get_client_orders(self.username)
        if not pedidos:
            print("No hay pedidos o error al consultar.\n")
            return
        print(f"Pedidos de '{self.username}':")
        for p in pedidos:
            print(f" - ID: {p['pedido_id']}, Estado: {p['estado']}, Total: {p['total']}")
            for prod in p['productos']:
                print(f"     -> {prod['id']} | {prod['nombre']} | {prod['precio']}")
        print()

    def cancelar_pedido(self):
        print("\n[Cancelar Pedido]")
        order_id = input("ID del pedido a cancelar: ").strip()
        if not order_id:
            print("No se ingresó un ID de pedido.\n")
            return
        ok, msg = self.controller.cancel_order(order_id)
        if ok:
            print(f"Cancelación exitosa. {msg}\n")
        else:
            print(f"Cancelación fallida: {msg}\n")

    def enviar_a_robot(self):
        print("\n[Enviar pedido al Robot]")
        pedido_id = input("ID del pedido que ya existe: ").strip()
        if not pedido_id:
            print("ID de pedido no válido.")
            return

        pedidos = self.controller.get_client_orders(self.username)
        matching = [p for p in pedidos if p["pedido_id"] == pedido_id]
        if not matching:
            print("No existe un pedido con ese ID.")
            return
        productos = matching[0]["productos"]
        self.controller.send_to_robot(pedido_id, productos)
        print(f"Pedido '{pedido_id}' enviado al Robot.\n")

    def enviar_a_repartidor(self):
        print("\n[Enviar pedido al Repartidor]")
        pedido_id = input("ID del pedido: ").strip()
        direccion = input("Dirección de entrega: ").strip() 
        if not pedido_id or not direccion:
            print("ID de pedido o dirección no válidos.")
            return
        pedidos = self.controller.get_client_orders(self.username)
        match = [p for p in pedidos if p["pedido_id"] == pedido_id]
        if not match:
            print("No existe un pedido con ese ID en tu usuario.")
            return
        productos = match[0]["productos"]
        self.controller.send_to_repartidor(pedido_id, direccion, productos)
        print(f"Pedido '{pedido_id}' enviado al Repartidor. Dirección: {direccion}\n")

    def _mostrar_menu_principal(self):
        """
        Muestra las opciones disponibles al usuario.
        """
        print("=" * 40)
        print("Saimazoom CLI - Menú Principal")
        print("1. Registrar Cliente")
        print("2. Iniciar Sesión")
        print("3. Realizar Pedido")
        print("4. Consultar Pedidos")
        print("5. Cancelar Pedido")
        print("6. Enviar Pedido al Robot")
        print("7. Enviar Pedido al Repartidor")
        print("Q. Salir")
        print("=" * 40)