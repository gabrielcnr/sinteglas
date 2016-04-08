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


def test_igualdade():
    esp1 = Especificacao(largura=60, comprimento=90, espessura=2.4)
    esp2 = Especificacao(largura=60, comprimento=90, espessura=2.4)

    assert esp1 is not esp2
    assert esp1 == esp2


def test_desigualdade():
    esp1 = Especificacao(largura=60, comprimento=90, espessura=2.4)
    esp2 = Especificacao(largura=70, comprimento=115, espessura=2.4)

    assert esp1 != esp2


def test_from_string():
    esp = Especificacao.from_string('110x210|5,56')
    assert esp.largura == 110
    assert esp.comprimento == 210
    assert esp.espessura == 5.56


def test_from_string_invalid():
    with pytest.raises(ValueError):
        Especificacao.from_string('1,10x210|5,56')
