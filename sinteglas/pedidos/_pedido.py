from atom.api import Atom, Typed, Int, Str, Unicode, List
import datetime


class StatusPedido(object):
    VAZIO = 'VAZIO'
    ABERTO = 'ABERTO'
    PARCIAL = 'PARCIAL'
    NAO_INICIADO = 'NAO_INICIADO'
    COMPLETO = 'COMPLETO'
    CONCLUIDO = 'CONCLUIDO'


class EntregaItemPedido(Atom):
    quantidade = Int()
    data_entrada = Typed(datetime.datetime)


class ItemPedido(Atom):
    op_id = Int()
    item_id = Int()
    quantidade = Int()
    data_entrada = Typed(datetime.datetime)

    entregas = List()

    def adicionar_entrega(self, quantidade):
        if quantidade > self.total_restante:
            raise RuntimeError('entrega excedente')

        entrega = EntregaItemPedido(
            quantidade=quantidade,
            data_entrada=data_hora_atual(),
        )
        self.entregas.append(entrega)

    @property
    def total_entregue(self):
        return sum((e.quantidade for e in self.entregas), 0)

    @property
    def total_restante(self):
        return self.quantidade - self.total_entregue

    @property
    def status(self):
        if self.total_entregue == self.quantidade:
            return StatusPedido.COMPLETO
        elif self.total_entregue == 0:
            return StatusPedido.NAO_INICIADO
        else:
            return StatusPedido.PARCIAL


class Pedido(Atom):
    # campos obrigatorios
    op_id = Int()
    data_entrada = Typed(datetime.datetime)
    cliente = Unicode()

    prazo = Int()

    # observacoes = List() # lista de observacoes

    itens = List()  # lista de items de pedido

    @classmethod
    def criar_novo(cls, op_id, cliente):
        pedido = cls()
        pedido.op_id = op_id
        pedido.cliente = cliente
        pedido.data_entrada = data_hora_atual()
        return pedido

    def adicionar_item(self, quantidade):
        item = ItemPedido()
        item.quantidade = quantidade
        item.data_entrada = data_hora_atual()
        self.itens.append(item)

    @property
    def status(self):
        if not self.itens:
            return StatusPedido.VAZIO
        else:
            concluido = all((i.status == StatusPedido.COMPLETO
                             for i in self.itens))
            return StatusPedido.CONCLUIDO if concluido else StatusPedido.ABERTO


def data_hora_atual():
    return datetime.datetime.now()
