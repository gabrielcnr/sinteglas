import datetime

import mock
import pytest
from sinteglas.pedidos import Pedido, StatusPedido


@mock.patch('sinteglas.pedidos._pedido.data_hora_atual')
def test_criar_novo_pedido(mock_data_hora_atual):
    dt = datetime.datetime(2016, 3, 6, 11, 0)
    mock_data_hora_atual.return_value = dt
    pedido = criar_pedido_teste()

    assert pedido.op_id == 123
    assert pedido.cliente == 'Gabriel'
    assert pedido.data_entrada == dt

    assert pedido.status == StatusPedido.VAZIO


def test_adicionar_item_de_pedido():
    pedido = criar_pedido_teste()

    pedido.adicionar_item(
        quantidade=10,
    )

    assert len(pedido.itens) == 1

    assert pedido.itens[0].quantidade == 10

    assert pedido.status == StatusPedido.ABERTO


def test_adicionar_entrega_parcial():
    pedido = criar_pedido_teste()

    pedido.adicionar_item(
        quantidade=10,
    )

    [item] = pedido.itens

    item.adicionar_entrega(
        quantidade=4
    )

    assert item.total_entregue == 4
    assert item.total_restante == 6
    assert item.status == StatusPedido.PARCIAL


def test_multiplas_entregas_item_completo():
    pedido = criar_pedido_teste()

    pedido.adicionar_item(
        quantidade=10,
    )

    [item] = pedido.itens

    item.adicionar_entrega(
        quantidade=4
    )

    item.adicionar_entrega(
        quantidade=6
    )

    assert item.total_entregue == 10
    assert item.total_restante == 0
    assert item.quantidade == 10

    assert item.status == StatusPedido.COMPLETO


def test_pedido_com_dois_itens_um_deles_entregue_completo_outro_parcial():
    pedido = criar_pedido_teste()

    pedido.adicionar_item(
        quantidade=10,
    )

    pedido.adicionar_item(
        quantidade=20,
    )

    [item1, item2] = pedido.itens

    item1.adicionar_entrega(
        quantidade=4
    )

    item1.adicionar_entrega(
        quantidade=6
    )

    item2.adicionar_entrega(
        quantidade=12
    )

    assert item1.status == StatusPedido.COMPLETO
    assert item2.status == StatusPedido.PARCIAL

    assert pedido.status == StatusPedido.ABERTO

    item2.adicionar_entrega(
        quantidade=8
    )

    assert pedido.status == StatusPedido.CONCLUIDO


def test_entrega_excedente():
    pedido = criar_pedido_teste()

    pedido.adicionar_item(
        quantidade=10,
    )

    [item] = pedido.itens

    item.adicionar_entrega(
        quantidade=4
    )

    with pytest.raises(RuntimeError):
        item.adicionar_entrega(
            quantidade=7
        )


@mock.patch('sinteglas.pedidos._pedido.data_hora_atual')
@mock.patch('getpass.getuser')
def test_observacao_pedido(mock_getuser, mock_data_hora_atual):
    dt = datetime.datetime(2016, 2, 17, 20, 21)

    mock_getuser.return_value = 'joao'
    mock_data_hora_atual.return_value = dt

    pedido = criar_pedido_teste()
    assert pedido.observacoes == []

    pedido.adicionar_observacao('Isto eh um teste')

    [obs] = pedido.observacoes

    assert obs.texto == 'Isto eh um teste'
    assert obs.autor == 'joao'
    assert obs.data_hora == dt
    assert obs.op_id == pedido.op_id


def criar_pedido_teste():
    pedido = Pedido.criar_novo(
        op_id=123,
        cliente='Gabriel',
    )
    return pedido
