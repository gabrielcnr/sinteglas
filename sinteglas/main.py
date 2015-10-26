import enaml
from enaml.qt.qt_application import QtApplication
from sinteglas.controller import SinteglasOrderController
from sinteglas.model import create_database_session

with enaml.imports():
    from sinteglas.views.main import Main


def main():
    app = QtApplication()
    session = create_database_session()
    controller = SinteglasOrderController(session=session)
    controller.populate_demo_database()
    view = Main(controller=controller)
    view.show()
    app.start()


if __name__ == '__main__':
    main()
