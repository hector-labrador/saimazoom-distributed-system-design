#!/bin/bash
#
# run_actors.sh
# -------------
# Este script lanza Robot, Repartidor y Controller en segundo plano
# y espera a que el usuario pulse Enter para detenerlos.
#
# Requisitos:
#  - Python 3


# Creamos carpeta de logs si no existe
mkdir -p logs

echo "=== Starting Robot in background... ==="
python src/launch_robot.py > logs/robot.log 2>&1 &
ROBOT_PID=$!
echo "Robot corriendo con PID $ROBOT_PID (logs en logs/robot.log)"

echo "=== Starting Repartidor in background... ==="
python src/launch_delivery.py > logs/repartidor.log 2>&1 &
REPARTIDOR_PID=$!
echo "Repartidor corriendo con PID $REPARTIDOR_PID (logs en logs/repartidor.log)"

echo "=== Starting Controller in background... ==="
python src/launch_controller.py > logs/controller.log 2>&1 &
CONTROLLER_PID=$!
echo "Controller corriendo con PID $CONTROLLER_PID (logs en logs/controller.log)"

echo ""
echo "=== Todos los actores se han lanzado. Presiona Enter para detenerlos. ==="
read

echo "=== Deteniendo todos los actores... ==="
kill $ROBOT_PID $REPARTIDOR_PID $CONTROLLER_PID 2>/dev/null
sleep 1
echo "=== Hecho. ==="
