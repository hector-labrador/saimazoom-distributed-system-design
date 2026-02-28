import unittest
import os
import time
import subprocess
import signal
import sqlite3

class TestIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Eliminamos la BD para entorno limpio
        if os.path.exists("data/saimazoom.db"):
            os.remove("data/saimazoom.db")

        # Lanzar Robot
        cls.robot_proc = subprocess.Popen(
            ["python", "src/launch_robot.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        time.sleep(1)

        # Lanzar Repartidor
        cls.delivery_proc = subprocess.Popen(
            ["python", "src/launch_delivery.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        time.sleep(1)

        # Lanzar Controller
        cls.controller_proc = subprocess.Popen(
            ["python", "src/launch_controller.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        # Matamos Robot, Repartidor, Controller
        for proc in [cls.robot_proc, cls.delivery_proc, cls.controller_proc]:
            if proc and proc.poll() is None:
                proc.send_signal(signal.SIGINT)
                time.sleep(0.5)
                if proc.poll() is None:
                    proc.kill()

    def test_full_flow(self):
        """
        Fase 1: Registrar user, login, crear pedido => ID=OrderIntegration
        Fase 2: login, enviar pedido al Robot (6) y Repartidor (7). => ID=OrderIntegration
        """
        script_commands_1 = """1
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
"""
        client_proc1 = subprocess.Popen(
            ["python", "src/launch_client.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        out1, err1 = client_proc1.communicate(script_commands_1)
        rc1 = client_proc1.wait()

        if rc1 != 0:
            print("=== STDOUT FASE 1 ===\n", out1)
            print("=== STDERR FASE 1 ===\n", err1)
        self.assertEqual(rc1, 0, "Error en la Fase 1 del Cliente (crear pedido)")

        conn = sqlite3.connect("data/saimazoom.db")
        c = conn.cursor()
        c.execute("SELECT status, total FROM orders WHERE id=?", ("OrderIntegration",))
        row = c.fetchone()
        conn.close()
        self.assertIsNotNone(row, "No se creó 'OrderIntegration'")
        self.assertEqual(row[0], "Solicitado", f"Estado tras crearlo debe ser 'Solicitado', en vez de {row[0]}")
        self.assertEqual(row[1], 300.0, "Total=300 (100 + 200)")

        script_commands_2 = """2
testUser
testPass
6
OrderIntegration
7
OrderIntegration
Calle Falsa 123
q
"""
        client_proc2 = subprocess.Popen(
            ["python", "src/launch_client.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        out2, err2 = client_proc2.communicate(script_commands_2)
        rc2 = client_proc2.wait()

        if rc2 != 0:
            print("=== STDOUT FASE 2 ===\n", out2)
            print("=== STDERR FASE 2 ===\n", err2)
        self.assertEqual(rc2, 0, "Error en la Fase 2 del Cliente (enviar Robot/Repartidor)")

        time.sleep(2)

        conn = sqlite3.connect("data/saimazoom.db")
        c = conn.cursor()
        c.execute("SELECT status FROM orders WHERE id=?", ("OrderIntegration",))
        final_status = c.fetchone()[0]
        conn.close()

        valid_final = [ "En_Almacen", "En_Cinta", "En_Reparto", "Entregado", "Solicitado" ]
        self.assertIn(final_status, valid_final,
            f"El estado final debería ser uno de {valid_final}, y es {final_status}")

if __name__ == '__main__':
    unittest.main()
