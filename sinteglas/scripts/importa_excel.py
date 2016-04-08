from collections import OrderedDict

import pandas as pd

from sinteglas.pedidos import Pedido
from sinteglas.pedidos.especificacao import Especificacao
import pdb


def main():
    df = pd.read_excel('/Users/gabriel/Downloads/SINTEGLAS.xlsx', header=0)

    corridos_index = list(df.columns).index('CORRIDOS')

    df = df[df.columns[:corridos_index + 1]]

    pedidos = OrderedDict()

    df['OBSERVACOES'].fillna('', inplace=True)
    df['OK'].fillna(0, inplace=True)

    for _, row in df.iterrows():
        pedido = obter_pedido(pedidos, row)
        item = pedido.adicionar_item(
            quantidade=int(row['QTDE']),
            especificacao=Especificacao.from_string(row['ESP x TAM'].strip()),
        )
        if row['OK']:
            item.adicionar_entrega(int(row['OK']))

        if row['OBSERVACOES']:
            try:
                pedido.adicionar_observacao(row['OBSERVACOES'])
            except Exception as ex:
                print repr(ex)
                pdb.set_trace()

    return pedidos


def obter_pedido(pedidos, row):
    op_id = row['OP']
    if op_id in pedidos:
        pedido = pedidos[row['OP']]
    else:
        pedido = Pedido.criar_novo(
            cliente=row['CLIENTE'],
            op_id=op_id,
        )
        pedidos[op_id] = pedido
    return pedido


if __name__ == '__main__':
    pedidos = main()
    for op_id, pedido in pedidos.items():
        print 'Pedido <OP: {!r}, Cliente: {}>'.format(pedido.op_id,
                                                      pedido.cliente)
        for item in pedido.itens:
            print '    Item <Qtd: {!r}, Especificacao: {}'.format(
                item.quantidade, item.especificacao,
            )
        print
    pdb.set_trace()
