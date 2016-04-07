PESO_ESPECIFICO_ACRILICO = 1.19


tamanhos = [(60, 90), (70, 115),
            (110, 210), (135, 185), ]

espessuras = [1.00, 1.30, 1.60, 2.00, 2.40, 3.20, 4.00, 4.75,
              5.56, 6.35, 8.00, 10.00, 12.70, 15.90, 19.05, 25.40]


class Medidas(object):
    def __init__(self, largura, comprimento, espessura):
        assert (largura, comprimento) in tamanhos, 'tamanho (LxC) invalido'
        assert espessura in espessuras, 'espessura invalida'
        self.largura = largura  # cm
        self.comprimento = comprimento  # cm
        self.espessura = espessura  # mm

    @property
    def peso(self):
        return ((self.largura / 100.) * (self.comprimento / 100.) *
                self.espessura * PESO_ESPECIFICO_ACRILICO)

    def __str__(self):
        espessura = '{:.2f}'.format(self.espessura)
        espessura = espessura.replace('.', ',')
        return '{}x{}|{}'.format(self.largura, self.comprimento, espessura)
