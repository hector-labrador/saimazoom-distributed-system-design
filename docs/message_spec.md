# Especificación de Mensajes (Saimazoom)

En este documento se describe el **formato de mensajes** que se intercambiarán entre los distintos actores del sistema Saimazoom (Cliente, Controlador, Robot, Repartidor), usando RabbitMQ como broker de mensajería.

---

## 1. Mensajes de Cliente -> Controlador

1. **Registro de Cliente**  
   - **Acción**: `REGISTER`
   - **Formato** (JSON):
     ```json
     {
       "accion": "REGISTER",
       "datos": {
         "nombre": "<nombre_cliente>",
         "contrasenia": "<password>"
       }
     }
     ```
   - **Respuesta** (éxito):
     ```json
     {
       "accion": "REGISTERED",
       "estado": "OK",
       "mensaje": "Cliente registrado correctamente"
     }
     ```
   - **Respuesta** (error):
     ```json
     {
       "accion": "REGISTERED",
       "estado": "ERROR",
       "mensaje": "Ya existe un cliente con ese nombre"
     }
     ```

2. **Inicio de Sesión**  
   - **Acción**: `LOGIN`
   - **Formato** (JSON):
     ```json
     {
       "accion": "LOGIN",
       "datos": {
         "nombre": "<nombre_cliente>",
         "contrasenia": "<password>"
       }
     }
     ```
   - **Respuesta** (éxito):
     ```json
     {
       "accion": "LOGGED",
       "estado": "OK",
       "mensaje": "Sesión iniciada"
     }
     ```
   - **Respuesta** (error):
     ```json
     {
       "accion": "LOGGED",
       "estado": "ERROR",
       "mensaje": "Credenciales inválidas"
     }
     ```

3. **Realizar Pedido**  
   - **Acción**: `PLACE_ORDER`
   - **Formato**:
     ```json
     {
       "accion": "PLACE_ORDER",
       "datos": {
         "pedido_id": "<uuid_o_id_unico>",
         "cliente_id": "<nombre_cliente>",
         "productos": [
           {
             "id": "...",
             "nombre": "...",
             "precio": 0.0
           }
         ]
       }
     }
     ```
   - **Respuesta** (éxito):
     ```json
     {
       "accion": "ORDER_PLACED",
       "estado": "OK",
       "mensaje": "Pedido registrado en el sistema"
     }
     ```
   - **Respuesta** (error):
     ```json
     {
       "accion": "ORDER_PLACED",
       "estado": "ERROR",
       "mensaje": "Cliente no registrado"
     }
     ```

4. **Consultar Pedidos**  
   - **Acción**: `GET_ORDERS`
   - **Formato**:
     ```json
     {
       "accion": "GET_ORDERS",
       "cliente_id": "<nombre_cliente>"
     }
     ```
   - **Respuesta** (éxito):
     ```json
     {
       "accion": "ORDERS_LIST",
       "estado": "OK",
       "pedidos": [
         {
           "pedido_id": "<pedido_id>",
           "estado": "<estado_pedido>",
           "productos": [
             {
               "id": "...",
               "nombre": "...",
               "precio": 0.0
             }
           ],
           "total": 0.0
         }
       ]
     }
     ```
   - **Respuesta** (error):
     ```json
     {
       "accion": "ORDERS_LIST",
       "estado": "ERROR",
       "mensaje": "Error al consultar pedidos"
     }
     ```

5. **Cancelar Pedido**  
   - **Acción**: `CANCEL_ORDER`
   - **Formato**:
     ```json
     {
       "accion": "CANCEL_ORDER",
       "pedido_id": "<pedido_id>"
     }
     ```
   - **Respuesta** (éxito):
     ```json
     {
       "accion": "ORDER_CANCELED",
       "estado": "OK",
       "mensaje": "Pedido cancelado"
     }
     ```
   - **Respuesta** (error):
     ```json
     {
       "accion": "ORDER_CANCELED",
       "estado": "ERROR",
       "mensaje": "No se puede cancelar el pedido en su estado actual"
     }
     ```

---

## 2. Mensajes Controlador -> Robot

1. **Mover Producto**  
   - **Acción**: `MOVE_PRODUCT`
   - **Formato** (JSON):
     ```json
     {
       "accion": "MOVE_PRODUCT",
       "pedido_id": "<pedido_id>",
       "productos": [
         {
           "id": "<id_producto>",
           "nombre": "<nombre_producto>",
           "precio": 0.0
         }
       ]
     }
     ```
   - **Respuesta** (Robot -> Controlador):
     ```json
     {
       "accion": "PRODUCT_MOVED",
       "pedido_id": "<pedido_id>",
       "productos_encontrados": [
         {
           "id": "<id_producto>",
           "nombre": "<nombre_producto>",
           "precio": 0.0
         }
       ],
       "productos_no_encontrados": [
         {
           "id": "<id_producto>",
           "nombre": "<nombre_producto>",
           "precio": 0.0
         }
       ]
     }
     ```

---

## 3. Mensajes Controlador -> Repartidor

1. **Repartir Producto**  
   - **Acción**: `DELIVER_PRODUCT`
   - **Formato** (JSON):
     ```json
     {
       "accion": "DELIVER_PRODUCT",
       "pedido_id": "<pedido_id>",
       "direccion": "<direccion_cliente>",
       "productos": [
         {
           "id": "<id_producto>",
           "nombre": "<nombre_producto>",
           "precio": 0.0
         }
       ]
     }
     ```
   - **Respuesta** (Repartidor -> Controlador):
     ```json
     {
       "accion": "PRODUCT_DELIVERED",
       "pedido_id": "<pedido_id>",
       "entregado": true,
       "intentos_usados": 2
     }
     ```

---
