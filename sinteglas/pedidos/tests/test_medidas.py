import pytest

from sinteglas.pedidos.medidas import Medidas


def test_peso_da_medida():
    medida = Medidas(
        largura=70,
        comprimento=115,
        espessura=2.4,
    )

    assert round(medida.peso, 3) == 2.299


def test_representacao_textual_da_medida():
    medida = Medidas(
        largura=70,
        comprimento=115,
        espessura=2.4,
    )

    assert '70x115|2,40' == str(medida)


def test_medida_invalida():
    # largura invalida
    with pytest.raises(AssertionError):
        Medidas(largura=20, comprimento=115, espessura=2.4)

    # comprimento invalido
    with pytest.raises(AssertionError):
        Medidas(largura=70, comprimento=22, espessura=2.4)

    # espessura invalida
    with pytest.raises(AssertionError):
        Medidas(largura=70, comprimento=115, espessura=12.25)
