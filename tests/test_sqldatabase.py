import unittest
import os
from saimazoom_lib.sqldatabase import (
    create_connection,
    create_table_clients,
    insert_client,
    find_client,
    create_table_orders,
    insert_order,
    get_orders_by_client,
    update_order_status,
    get_order_status
)

class TestSqlDatabase(unittest.TestCase):
    def setUp(self):
        if os.path.exists("data/saimazoom.db"):
            os.remove("data/saimazoom.db")
        create_table_clients()
        create_table_orders()

    def test_insert_and_find_client(self):
        res = insert_client("testuser", "testpass")
        self.assertTrue(res)
        found = find_client("testuser", "testpass")
        self.assertTrue(found)

        res2 = insert_client("testuser", "otra_pass")
        self.assertFalse(res2)

    def test_insert_and_get_order(self):
        insert_client("testuser2", "pass2")
        inserted = insert_order(
            order_id="ORDER-1",
            client_username="testuser2",
            products=[{"id":"P1","nombre":"N1","precio":100}],
            status="Solicitado"
        )
        self.assertTrue(inserted)
        orders = get_orders_by_client("testuser2")
        self.assertEqual(len(orders), 1)
        self.assertEqual(orders[0]["pedido_id"], "ORDER-1")
        self.assertEqual(orders[0]["estado"], "Solicitado")

        status = get_order_status("ORDER-1")
        self.assertEqual(status, "Solicitado")

        updated = update_order_status("ORDER-1", "En_Almacen")
        self.assertTrue(updated)
        status2 = get_order_status("ORDER-1")
        self.assertEqual(status2, "En_Almacen")

if __name__ == '__main__':
    unittest.main()
