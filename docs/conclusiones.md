# Conclusiones

## Conclusiones Técnicas

1. _Arquitectura distribuida con RabbitMQ:_
   - Se ha demostrado la utilidad de RabbitMQ para la comunicación asíncrona entre los distintos actores (Controlador, Robot, Repartidor).
   - La configuración de colas permite una escalabilidad sencilla si se añaden más robots o repartidores.
2. _Persistencia en SQLite:_
   - Permite un desarrollo rápido, sin necesidad de un servidor de BBDD aparte.
   - Es suficiente para el volumen de datos de la práctica.
3. _Control de estados de pedidos:_
   - Se ha implementado un flujo realista de estados (Solicitado, En_Almacen, En_Cinta, En_Reparto, Entregado, Cancelado).
   - El uso de funciones como progress_order_state simplifica la validación de transiciones.
4. _Test unitarios e integración:_
   - Se han creado tests de base de datos, Controller, Robot y Repartidor.
   - Aún cabe mejorar la cobertura para aspectos más integrales (p.ej. encolado real y correlación de mensajes).
5. _Metodologías de Logging y Configuración:_
   - Se ha usado la librería logging para un control granular de logs (INFO, WARNING, DEBUG...).
   - configparser para server.conf facilita cambiar el host/puerto sin modificar código.

---

## Conclusiones Personales

1. _Aprendizaje en mensajería con RabbitMQ:_
   - Ha sido muy instructivo dominar la conexión, declaración de colas y consumo de mensajes.
   - Se comprende mejor la naturaleza asíncrona y la importancia de los “ack” en RabbitMQ.
2. _Dominio de persistencia con SQLite:_
   - Ayuda a ver cómo se diseña un esquema básico (tablas clients, orders) y la interacción vía Python (sqlite3).
3. _Trabajo en equipo y organización del repositorio:_
   - Git y los commits granulares han servido para trazar la evolución del proyecto de manera clara.
   - El uso de pruebas unitarias incrementales ha facilitado detectar errores rápidamente.
4. _Dificultades encontradas:_
   - Manejo de estados en un sistema distribuido puede volverse complejo: conviene diseñar cuidadosamente la lógica de estados y los mensajes que actualizan cada paso.
   - Configurar import paths y la ejecución de tests (PYTHONPATH, Makefile) puede ser tedioso.
5. _Sugerencias futuras:_
   - Implementar un sistema de correlación de mensajes para que el Robot y el Repartidor devuelvan notificaciones al Controller y este actualice el estado final.
   - Sustituir SQLite por una base de datos robusta (PostgreSQL) si se escalase la aplicación.
   - Mejorar la interfaz de usuario (por ejemplo, con una sencilla GUI web).

---