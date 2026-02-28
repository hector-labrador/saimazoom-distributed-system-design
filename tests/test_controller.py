import unittest
import os
from saimazoom_lib.controller import Controller, ESTADO_SOLICITADO, ESTADO_CANCELADO
from saimazoom_lib.sqldatabase import create_table_clients, create_table_orders

class TestController(unittest.TestCase):
    def setUp(self):
        if os.path.exists("data/saimazoom.db"):
            os.remove("data/saimazoom.db")
        create_table_clients()
        create_table_orders()
        self.controller = Controller()

    def test_register_and_login(self):
        res = self.controller.register_client("userA","passA")
        self.assertTrue(res)
        login_ok = self.controller.login_client("userA","passA")
        self.assertTrue(login_ok)

        res2 = self.controller.register_client("userA","otro_pass")
        self.assertFalse(res2)

    def test_place_and_cancel_order(self):
        self.controller.register_client("userB","passB")
        placed = self.controller.place_order("ORD-100", "userB", [{"id":"P1","nombre":"Prod","precio":50}])
        self.assertTrue(placed)
        orders = self.controller.get_client_orders("userB")
        self.assertEqual(len(orders),1)
        self.assertEqual(orders[0]["pedido_id"],"ORD-100")
        self.assertEqual(orders[0]["estado"],ESTADO_SOLICITADO)

        ok, msg = self.controller.cancel_order("ORD-100")
        self.assertTrue(ok)
        self.assertIn("cancelado", msg.lower())

        ok2, msg2 = self.controller.cancel_order("ORD-XYZ")
        self.assertFalse(ok2)

if __name__ == '__main__':
    unittest.main()
