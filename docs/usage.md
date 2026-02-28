# Guía de Uso y Arquitectura de Saimazoom

## 1. Arquitectura del Proyecto

El proyecto se compone de:

- _Controller_: Orquesta la lógica de negocio y comunicación con la base de datos (SQLite).
- _Cliente CLI_ (ClienteCLI): Permite a un usuario registrarse, iniciar sesión, gestionar y consultar pedidos, y enviar pedidos al robot y repartidor.
- _Robot_: Encargado de mover productos del almacén a la cinta transportadora.
- _Repartidor_: Entrega los productos a la dirección del cliente.

La comunicación entre Controller, Robot y Repartidor se realiza con _RabbitMQ_, usando colas:

- saimazoom_robot_queue
- saimazoom_repartidor_queue

La persistencia de clientes y pedidos se realiza en un fichero SQLite data/saimazoom.db.

---

## 2. Pasos de Ejecución

1. _Instalar Dependencias_\
   Asegúrate de tener Python 3.x y la librería pika instalada. Por ejemplo:

   ```bash
   pip install pika
   
   ```

Además, RabbitMQ debe estar disponible (local o remoto).

```
Configurar el Proyecto

    Edita config/server.conf para ajustar los parámetros de conexión (RabbitMQ host, puerto, usuario, password), y el nivel de logs (INFO, DEBUG...).

    Verifica que en data/ puedas escribir la base de datos saimazoom.db.

Iniciar el Robot
Desde la raíz del proyecto, puedes usar el Makefile (Commit 25) o Python directamente:
```

make run_robot o python src/launch_robot.py

El robot permanecerá a la espera de órdenes de mover productos.

Iniciar el Repartidor en otra terminal:

make run_repartidor o python src/launch_delivery.py

El repartidor esperará órdenes de entregar productos.

Iniciar el Controller en otra terminal:

make run_controller o python src/launch_controller.py

El Controller conectará a RabbitMQ, declarará colas y quedará listo para recibir peticiones (en este proyecto, las peticiones vendrán del Cliente CLI).

Ejecutar el Cliente en otra terminal:

make run_client o python src/launch_client.py

Aparecerá un menú donde podrás:

```
Registrar cliente

Iniciar sesión

Realizar pedido

Consultar pedidos

Cancelar pedido

Enviar pedido al Robot (lo pasará de estado Solicitado a En_Almacen y generará un mensaje MOVE_PRODUCT a la cola Robot)

Enviar pedido al Repartidor (lo pasará de En_Cinta a En_Reparto y mandará DELIVER_PRODUCT a la cola Repartidor)
```

Comprobar Resultados

```
Observa las ventanas del Robot y Repartidor. Deberían imprimir logs en tiempo real cuando reciben mensajes.

Observa el Controller, que imprime logs según la configuración de server.conf.

Consulta la base de datos en data/saimazoom.db para ver clientes y pedidos.
```