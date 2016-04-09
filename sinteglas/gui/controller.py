from atom.api import Atom, List, Typed, observe

from sinteglas.pedidos import Pedido
from sinteglas.pedidos._pedido import ItemPedido


class PedidosController(Atom):
    pedidos = List(Pedido)
    pedido_selecionado = Typed(Pedido)
    itens_de_pedido = List(ItemPedido)

    @observe('pedido_selecionado')
    def atualizar_itens_de_pedido_para_o_pedido_selecionado(self, change=None):
        if self.pedido_selecionado:
            self.itens_de_pedido = self.pedido_selecionado.itens
        else:
            self.itens_de_pedido = []
