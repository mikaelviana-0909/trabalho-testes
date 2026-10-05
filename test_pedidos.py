import unittest
from unittest.mock import Mock

from sistema import Estoque, Pedido


class TestPedido(unittest.TestCase):

    def setUp(self):
        self.estoque = Estoque()
        self.email_service = Mock()
        self.pedido = Pedido(
            self.estoque,
            self.email_service
        )

    def tearDown(self):
        pass

    # ---------- Estoque.buscar ----------

    def test_buscar_produto_existente(self):
        produto = self.estoque.buscar(1)

        self.assertEqual(produto["nome"], "Notebook")
        self.assertEqual(produto["preco"], 3000.00)
        self.assertEqual(produto["estoque"], 10)

    def test_buscar_produto_inexistente(self):
        with self.assertRaises(ValueError):
            self.estoque.buscar(99)

    # ---------- Estoque.baixar ----------

    def test_baixar_quantidade_valida(self):
        resultado = self.estoque.baixar(2, 5)

        self.assertTrue(resultado)
        self.assertEqual(self.estoque.produtos[2]["estoque"], 15)

    def test_baixar_acima_do_estoque(self):
        with self.assertRaises(ValueError):
            self.estoque.baixar(2, 21)

    # ---------- Pedido.adicionar_item ----------

    def test_adicionar_item_quantidade_valida(self):
        self.pedido.adicionar_item(2, 2)

        self.assertEqual(len(self.pedido.itens), 1)
        self.assertEqual(self.pedido.itens[0]["produto_id"], 2)
        self.assertEqual(self.pedido.itens[0]["quantidade"], 2)
        self.assertEqual(self.pedido.itens[0]["preco"], 100.00)

    def test_adicionar_item_quantidade_zero(self):
        with self.assertRaises(ValueError):
            self.pedido.adicionar_item(2, 0)

    def test_adicionar_item_quantidade_negativa(self):
        with self.assertRaises(ValueError):
            self.pedido.adicionar_item(2, -1)

    def test_adicionar_item_acima_do_estoque(self):
        with self.assertRaises(ValueError):
            self.pedido.adicionar_item(2, 21)

    def test_adicionar_item_com_estoque_stub(self):
        estoque_stub = Mock()

        estoque_stub.buscar.return_value = {
            "nome": "Mouse",
            "preco": 100.00,
            "estoque": 10
        }

        pedido = Pedido(
            estoque_stub,
            self.email_service
        )

        pedido.adicionar_item(2, 2)

        self.assertEqual(pedido.itens[0]["produto_id"], 2)
        self.assertEqual(pedido.itens[0]["quantidade"], 2)
        self.assertEqual(pedido.itens[0]["preco"], 100.00)

    # ---------- Pedido.calcular_subtotal ----------

    def test_calcular_subtotal_um_item(self):
        self.pedido.adicionar_item(2, 2)

        subtotal = self.pedido.calcular_subtotal()

        self.assertEqual(subtotal, 200.00)

    def test_calcular_subtotal_varios_itens(self):
        self.pedido.adicionar_item(2, 2)
        self.pedido.adicionar_item(3, 1)

        subtotal = self.pedido.calcular_subtotal()

        self.assertEqual(subtotal, 400.00)

    # ---------- Pedido.calcular_desconto ----------

    def test_calcular_desconto_cupom_10(self):
        self.pedido.adicionar_item(2, 2)

        desconto = self.pedido.calcular_desconto("DESCONTO10")

        self.assertEqual(desconto, 20.00)

    def test_calcular_desconto_subtotal_acima_de_500(self):
        self.pedido.adicionar_item(1, 1)

        desconto = self.pedido.calcular_desconto()

        self.assertEqual(desconto, 150.00)

    def test_calcular_desconto_subtotal_menor_500(self):
        self.pedido.adicionar_item(3, 2)

        desconto = self.pedido.calcular_desconto()

        self.assertEqual(desconto, 0)

    # ---------- Pedido.calcular_frete ----------

    def test_calcular_frete_distancia_negativa(self):
        with self.assertRaises(ValueError):
            self.pedido.calcular_frete(-1)

    def test_calcular_frete_subtotal_300(self):
        self.pedido.adicionar_item(3, 1)
        self.pedido.adicionar_item(2, 1)

        frete = self.pedido.calcular_frete(20)

        self.assertEqual(frete, 0)

    def test_calcular_frete_distancia_10(self):
        frete = self.pedido.calcular_frete(10)

        self.assertEqual(frete, 15)

    def test_calcular_frete_entre_10_e_30(self):
        frete = self.pedido.calcular_frete(20)

        self.assertEqual(frete, 30)

    def test_calcular_frete_acima_de_30(self):
        frete = self.pedido.calcular_frete(31)

        self.assertEqual(frete, 50)

    # ---------- Pedido.finalizar ----------

    def test_finalizar_pedido_vazio(self):
        with self.assertRaises(ValueError):
            self.pedido.finalizar(
                "cliente@email.com",
                10
            )

    def test_finalizar_pedido_valido(self):
        self.pedido.adicionar_item(2, 2)

        resultado = self.pedido.finalizar(
            "cliente@email.com",
            10
        )

        self.assertEqual(resultado["status"], "confirmado")
        self.assertEqual(resultado["total"], 215.00)

    def test_finalizar_envia_email(self):
        self.pedido.adicionar_item(2, 2)

        self.pedido.finalizar("cliente@email.com", 10)

        self.email_service.enviar.assert_called_once_with(
            "cliente@email.com",
            "Pedido confirmado",
            "Total do pedido: R$ 215.00"
        )

    def test_finalizar_distancia_invalida_nao_baixa_estoque(self):
        estoque_inicial = self.estoque.produtos[2]["estoque"]

        self.pedido.adicionar_item(2, 2)

        with self.assertRaises(ValueError):
            self.pedido.finalizar(
                "cliente@email.com",
                -1
            )

        self.assertEqual(
            self.estoque.produtos[2]["estoque"],
            estoque_inicial
        )


if __name__ == "__main__":
    unittest.main()