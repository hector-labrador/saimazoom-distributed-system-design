#!/bin/bash
#
# run_demo.sh
# -----------
# Simula un flujo "real" en el cliente, redirigiendo entradas
# al script commandline_client.py o launch_client.py.
#
# Requisitos:
#  - Haber lanzado Robot, Repartidor y Controller (por ejemplo, con run_actors.sh)

echo "=== FASE 1: Registrar cliente, login y crear pedido ==="
python src/commandline_client.py <<EOF
1
testUser
testPass
2
testUser
testPass
3
OrderIntegration
P1
Prod1
100
P2
Prod2
200

q
EOF

echo ""
echo "=== FASE 2: Iniciar sesión de nuevo y enviar pedido al Robot y Repartidor ==="
python src/commandline_client.py <<EOF
2
testUser
testPass
6
OrderIntegration
7
OrderIntegration
Calle Falsa 123
q
EOF

echo ""
echo "=== Demo finalizado. Revisa los logs o la BD para ver resultados. ==="
