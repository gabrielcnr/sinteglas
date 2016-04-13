import getpass

from atom.api import Atom, List, Typed, observe

from sinteglas.pedidos import Pedido
from sinteglas.pedidos._pedido import ItemPedido
from sinteglas.pedidos.observacao import ObservacaoItemPedido


class PedidosController(Atom):
    pedidos = List(Pedido)
    pedido_selecionado = Typed(Pedido)
    itens_de_pedido = List(ItemPedido)
    item_de_pedido_selecionado = Typed(ItemPedido)
    observacoes_do_item_de_pedido_selecionado = List(ObservacaoItemPedido)

    @observe('pedido_selecionado')
    def atualizar_itens_de_pedido_para_o_pedido_selecionado(self, change=None):
        if self.pedido_selecionado:
            self.itens_de_pedido = self.pedido_selecionado.itens
        else:
            self.itens_de_pedido = []

    @observe('itens_de_pedido')
    def resetar_item_de_pedido_selecionado(self, change=None):
        self.item_de_pedido_selecionado = None

    @observe('item_de_pedido_selecionado')
    def atualizar_observacoes_do_item_de_pedido_selecionado(self, change=None):
        if self.item_de_pedido_selecionado:
            self.observacoes_do_item_de_pedido_selecionado = self.item_de_pedido_selecionado.observacoes[:]
        else:
            self.observacoes_do_item_de_pedido_selecionado = []

    def adicionar_observacao_ao_item_de_pedido_selecionado(self, obs):
        autor = getpass.getuser()
        self.item_de_pedido_selecionado.adicionar_observacao(obs, autor)
        self.atualizar_observacoes_do_item_de_pedido_selecionado()

