import enaml
from enaml.qt.qt_application import QtApplication

from sinteglas.gui.controller import PedidosController
from sinteglas.scripts.importa_excel import importa_pedidos_do_excel

with enaml.imports():
    from sinteglas.gui.view_pedido import PedidosView


def main():
    pedidos = importa_pedidos_do_excel()
    controller = PedidosController(pedidos=pedidos.values())
    app = QtApplication()
    view = PedidosView(controller=controller)
    view.center_on_screen()
    view.show()
    view.maximize()
    app.start()


if __name__ == '__main__':
    main()
