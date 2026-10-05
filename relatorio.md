# 13. Perguntas do relatório

## 6. Qual foi o caso de teste mais importante? Por quê?

O caso de teste mais importante foi:

`test_finalizar_distancia_invalida_nao_baixa_estoque`

Esse teste foi importante porque revelou um defeito na aplicação. Ele
verifica se, ao tentar finalizar um pedido com uma distância inválida, o
estoque permanece inalterado.

O teste esperava que o estoque continuasse com 20 unidades, mas o
resultado obtido foi 18 unidades. Isso mostrou que o sistema baixa o
estoque antes de validar a distância do pedido.

------------------------------------------------------------------------

## 7. Qual valor de borda apresentou maior risco?

O valor de borda que apresentou maior risco foi a distância de **10
km**, pois ela define a mudança entre as faixas de frete.

No sistema:

-   distância menor ou igual a 10 km → frete de R\$ 15;
-   distância entre 10 e 30 km → frete de R\$ 30;
-   distância acima de 30 km → frete de R\$ 50.

Foi realizado um teste específico com distância igual a 10 km para
verificar esse limite.

Outro limite importante foi o subtotal de **R\$ 300**, pois a partir
desse valor o frete passa a ser gratuito.

------------------------------------------------------------------------

## 8. Quais dependências foram isoladas e por quê?

Foram isoladas duas dependências:

-   **EmailService:** foi utilizado um Mock para evitar a execução real
    do serviço de e-mail e permitir verificar se o método `enviar()` foi
    chamado corretamente, com os argumentos esperados.
-   **Estoque:** foi utilizado um Mock configurado como Stub para
    controlar o resultado retornado pelo método `buscar()`, evitando
    depender do estoque real nesse teste.

O isolamento das dependências permite testar o comportamento do `Pedido`
de forma mais controlada e independente.

------------------------------------------------------------------------

## 9. Qual a diferença entre Stub e Mock no seu projeto?

O **Stub** é utilizado para fornecer respostas controladas para o código
que está sendo testado.

No projeto, o estoque foi utilizado como Stub ao definir manualmente o
retorno de `buscar()`:

``` python
estoque_stub.buscar.return_value = {
    "nome": "Mouse",
    "preco": 100.00,
    "estoque": 10
}
```

O **Mock** é utilizado principalmente para verificar interações com uma
dependência, como chamadas, quantidade de chamadas e argumentos.

No projeto, o `EmailService` foi substituído por um Mock e foi
verificado se `enviar()` foi chamado corretamente:

``` python
self.email_service.enviar.assert_called_once_with(
    "cliente@email.com",
    "Pedido confirmado",
    "Total do pedido: R$ 215.00"
)
```

------------------------------------------------------------------------

## 10. Você atingiu 100% de cobertura de linhas? E de branches?

Não foi atingido 100% de cobertura de linhas.

O resultado da cobertura foi:

``` text
sistema.py           63      1     26      0    99%
test_pedidos.py     106      1      2      1    98%
TOTAL               169      2     28      1    98%
```

Considerando o `sistema.py`, foram cobertos **99% das linhas**.

Em relação aos branches, foram cobertos **100%**, pois foram
identificados 26 branches e nenhum ficou parcialmente coberto:

``` text
Branch: 26
BrPart: 0
```

A única linha não coberta no `sistema.py` foi o `return True` do método
`EmailService.enviar()`. Isso ocorreu porque o serviço real foi
substituído por um Mock durante os testes.

------------------------------------------------------------------------

## 11. 100% de cobertura significa ausência de bugs? Explique.

Não.

100% de cobertura significa que as partes do código e os caminhos
analisados foram executados pelos testes. Isso não garante que todos os
comportamentos do sistema estejam corretos.

Neste trabalho, mesmo com **100% dos branches cobertos** e **99% das
linhas do `sistema.py` cobertas**, foi encontrado um defeito relacionado
à alteração do estoque quando a finalização do pedido falha.

Portanto, cobertura de código aumenta a confiança nos testes, mas não
significa que o sistema esteja livre de bugs.

------------------------------------------------------------------------

## 12. Qual defeito foi encontrado e qual teste o revelou?

Foi encontrado um defeito no processo de finalização do pedido.

Quando a distância informada é inválida, o sistema deveria rejeitar o
pedido sem alterar o estoque. Porém, o método `finalizar()` baixa
primeiro os produtos do estoque e somente depois calcula o frete.

O teste que revelou o defeito foi:

`test_finalizar_distancia_invalida_nao_baixa_estoque`

O teste utilizou:

-   Produto: Mouse;
-   Quantidade: 2;
-   Estoque inicial: 20 unidades;
-   Distância: `-1`.

### Resultado esperado

O sistema deveria lançar `ValueError` e manter o estoque com 20
unidades.

### Resultado obtido

O sistema lançou `ValueError`, mas o estoque foi reduzido para 18
unidades.

O teste apresentou:

``` text
AssertionError: 18 != 20
```

Isso confirma que o estoque foi alterado mesmo com a finalização do
pedido sendo rejeitada.
