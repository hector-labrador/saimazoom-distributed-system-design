import unittest
from unittest.mock import MagicMock, patch
from saimazoom_lib.robot import Robot

class TestRobot(unittest.TestCase):
    def test_mover_producto(self):
        robot = Robot(robot_id=1, prob_no_encontrar=0.0)
        with patch('time.sleep', return_value=None):
            robot.mover_producto("PROD-1")

    @patch('time.sleep', return_value=None)
    @patch('random.random', return_value=0.99)
    def test_simular_mover_productos_all_found(self, mock_random, mock_sleep):
        robot = Robot(robot_id=2, prob_no_encontrar=0.1)
        mock_channel = MagicMock()
        pedido_id = "PED1"
        productos = [{"id": "P1"}, {"id": "P2"}]

        robot.simular_mover_productos(pedido_id, productos, mock_channel)
        args, kwargs = mock_channel.basic_publish.call_args
        self.assertIn("body", kwargs)
        body = kwargs["body"]
        import json
        msg = json.loads(body)
        self.assertEqual(msg["accion"], "PRODUCT_MOVED")
        self.assertEqual(msg["pedido_id"], pedido_id)
        self.assertEqual(len(msg["productos_no_encontrados"]), 0)

    @patch('time.sleep', return_value=None)
    @patch('random.random', return_value=0.05)
    def test_simular_mover_productos_some_missing(self, mock_random, mock_sleep):
        robot = Robot(robot_id=3, prob_no_encontrar=1.0)
        mock_channel = MagicMock()
        pedido_id = "PED2"
        productos = [{"id":"PX"}, {"id":"PY"}]

        robot.simular_mover_productos(pedido_id, productos, mock_channel)
        args, kwargs = mock_channel.basic_publish.call_args
        body = kwargs["body"]
        import json
        msg = json.loads(body)
        self.assertEqual(msg["accion"], "PRODUCT_MOVED")
        self.assertEqual(len(msg["productos_encontrados"]), 0)
        self.assertEqual(len(msg["productos_no_encontrados"]), 2)

if __name__ == '__main__':
    unittest.main()
