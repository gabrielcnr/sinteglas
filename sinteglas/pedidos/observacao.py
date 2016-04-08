import datetime

from atom.api import Atom, Unicode, Typed, Int


class Observacao(Atom):
    texto = Unicode()
    autor = Unicode()
    data_hora = Typed(datetime.datetime)


class ObservacaoPedido(Observacao):
    op_id = Int()


class ObservacaoItemPedido(Observacao):
    item_id = Int()
