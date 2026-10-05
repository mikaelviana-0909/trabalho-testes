class Estoque:
    def __init__(self):
        self.produtos = {
            1: {"nome": "Notebook", "preco": 3000.00, "estoque": 10},
            2: {"nome": "Mouse", "preco": 100.00, "estoque": 20},
            3: {"nome": "Teclado", "preco": 200.00, "estoque": 5},
            4: {"nome": "Fone", "preco": 150.00, "estoque": 8},
        }

    def buscar(self, produto_id):
        if produto_id not in self.produtos:
            raise ValueError("Produto não encontrado")

        return self.produtos[produto_id]

    def baixar(self, produto_id, quantidade):
        produto = self.buscar(produto_id)

        if quantidade > produto["estoque"]:
            raise ValueError("Estoque insuficiente")

        produto["estoque"] -= quantidade
        return True


class EmailService:
    def enviar(self, destinatario, assunto, mensagem):
        # Simula o envio de um e-mail.
        return True


class Pedido:
    def __init__(self, estoque, email_service):
        self.estoque = estoque
        self.email_service = email_service
        self.itens = []

    def adicionar_item(self, produto_id, quantidade):
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser positiva")

        produto = self.estoque.buscar(produto_id)

        if quantidade > produto["estoque"]:
            raise ValueError("Estoque insuficiente")

        self.itens.append({
            "produto_id": produto_id,
            "quantidade": quantidade,
            "preco": produto["preco"]
        })

    def calcular_subtotal(self):
        total = 0

        for item in self.itens:
            total += item["preco"] * item["quantidade"]

        return total

    def calcular_desconto(self, cupom=None):
        subtotal = self.calcular_subtotal()

        if cupom == "DESCONTO10":
            return subtotal * 0.10

        if subtotal >= 500:
            return subtotal * 0.05

        return 0

    def calcular_frete(self, distancia):
        if distancia < 0:
            raise ValueError("Distância inválida")

        if self.calcular_subtotal() >= 300:
            return 0

        if distancia <= 10:
            return 15

        if distancia <= 30:
            return 30

        return 50

    def calcular_total(self, distancia, cupom=None):
        subtotal = self.calcular_subtotal()
        desconto = self.calcular_desconto(cupom)
        frete = self.calcular_frete(distancia)

        return subtotal - desconto + frete

    def finalizar(self, cliente_email, distancia, cupom=None):
        if not self.itens:
            raise ValueError("Pedido vazio")

        for item in self.itens:
            self.estoque.baixar(
                item["produto_id"],
                item["quantidade"]
            )

        total = self.calcular_total(distancia, cupom)

        self.email_service.enviar(
            cliente_email,
            "Pedido confirmado",
            f"Total do pedido: R$ {total:.2f}"
        )

        return {
            "status": "confirmado",
            "total": total
        }
