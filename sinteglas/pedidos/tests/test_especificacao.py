import pytest

from sinteglas.pedidos.especificacao import Especificacao


def test_peso_da_especificacao():
    especificacao = Especificacao(
        largura=70,
        comprimento=115,
        espessura=2.4,
    )

    assert round(especificacao.peso, 3) == 2.299


def test_representacao_textual_da_medida():
    especificacao = Especificacao(
        largura=70,
        comprimento=115,
        espessura=2.4,
    )

    assert '70x115|2,40' == str(especificacao)


def test_medida_invalida():
    # largura invalida
    with pytest.raises(AssertionError):
        Especificacao(largura=20, comprimento=115, espessura=2.4)

    # comprimento invalido
    with pytest.raises(AssertionError):
        Especificacao(largura=70, comprimento=22, espessura=2.4)

    # espessura invalida
    with pytest.raises(AssertionError):
        Especificacao(largura=70, comprimento=115, espessura=12.25)
