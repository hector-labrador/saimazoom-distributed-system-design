import unittest
from unittest.mock import MagicMock, patch
from saimazoom_lib.repartidor import Repartidor

class TestRepartidor(unittest.TestCase):
    @patch('time.sleep', return_value=None)
    @patch('random.random', return_value=0.99)
    def test_simular_entrega_exito(self, mock_rand, mock_sleep):
        repartidor = Repartidor(repartidor_id=10, max_intentos=3, prob_exito=1.0)
        mock_channel = MagicMock()
        pedido_id = "PED-ENTREGA"
        direccion = "Calle Falsa 123"
        productos = [{"id": "A"}]

        repartidor.simular_entrega(pedido_id, direccion, productos, mock_channel)
        args, kwargs = mock_channel.basic_publish.call_args
        body = kwargs["body"]
        import json
        msg = json.loads(body)
        self.assertEqual(msg["accion"], "PRODUCT_DELIVERED")
        self.assertTrue(msg["entregado"])
        self.assertEqual(msg["intentos_usados"], 1)

    @patch('time.sleep', return_value=None)
    @patch('random.random', return_value=0.0)
    def test_simular_entrega_fallo(self, mock_rand, mock_sleep):
        repartidor = Repartidor(repartidor_id=11, max_intentos=2, prob_exito=0.0)
        mock_channel = MagicMock()
        pedido_id = "PED-FAIL"
        direccion = "NoEntrega"
        productos = [{"id":"Z"}]

        repartidor.simular_entrega(pedido_id, direccion, productos, mock_channel)
        args, kwargs = mock_channel.basic_publish.call_args
        import json
        msg = json.loads(kwargs["body"])
        self.assertEqual(msg["accion"], "PRODUCT_DELIVERED")
        self.assertFalse(msg["entregado"])
        self.assertEqual(msg["intentos_usados"], 2)

if __name__ == '__main__':
    unittest.main()
