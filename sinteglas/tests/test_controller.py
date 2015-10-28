import datetime
from sinteglas.controller import SinteglasOrderController, \
    DemoSinteglasOrderController
from sinteglas.model import create_database_session, Order
import mock
import pytest


@pytest.fixture
def controller():
    session = create_database_session()
    controller = SinteglasOrderController(session=session)
    return controller


@mock.patch('sinteglas.controller.SinteglasOrderController.now')
@mock.patch('sinteglas.controller.SinteglasOrderController.get_user')
def test_create_order(mock_get_user, mock_now, controller):
    mock_get_user.return_value = 'edu.fiasco'
    mock_now.return_value = datetime.datetime(2015, 10, 20, 15, 30)

    order_params = controller.create_blank_order()
    order_params.client = 'Rodrigo Vila'
    order_params.description = '20 chapa acrilica verde limao'
    order_params.estimated_delivery_date = datetime.date(2015, 10, 27)

    controller.save_new_order(order_params)

    [order] = controller.session.query(Order).all()

    assert order.client == 'Rodrigo Vila'
    assert order.description == '20 chapa acrilica verde limao'
    assert order.created_by == 'edu.fiasco'
    assert order.created_date == datetime.datetime(2015, 10, 20, 15, 30)
    assert order.estimated_delivery_date == datetime.date(2015, 10, 27)


@mock.patch('sinteglas.controller.SinteglasOrderController.now')
@mock.patch('sinteglas.controller.SinteglasOrderController.get_user')
def test_conclude_order(mock_get_user, mock_now, controller):
    mock_get_user.return_value = 'edu.fiasco'
    mock_now.side_effect = [datetime.datetime(2015, 10, 20, 15, 30),
                            datetime.datetime(2015, 10, 26, 11, 0)]

    order_params = controller.create_blank_order()
    order_params.estimated_delivery_date = datetime.date(2015, 10, 27)
    controller.save_new_order(order_params)

    [order] = controller.session.query(Order).all()
    controller.conclude_order(order)

    [order] = controller.session.query(Order).all()
    assert order.created_date == datetime.datetime(2015, 10, 20, 15, 30)
    assert order.estimated_delivery_date == datetime.date(2015, 10, 27)
    assert order.delivery_date == datetime.date(2015, 10, 26)


def test_delete_order(controller):
    order_params = controller.create_blank_order()
    controller.save_new_order(order_params)

    [order] = controller.session.query(Order).all()
    controller.delete_order(order)

    [] == controller.session.query(Order).all()


def test_show_closed():
    session = create_database_session()
    controller = DemoSinteglasOrderController(session=session)
    controller.populate_demo_database()
    controller.load_orders()

    # Default should be do not show closed orders
    assert len(controller.orders) == 7
    assert len(controller.visible_orders) == 4

    controller.show_closed = True
    assert len(controller.visible_orders) == 7


def test_counts():
    session = create_database_session()
    controller = DemoSinteglasOrderController(session=session)
    controller.populate_demo_database()
    controller.load_orders()

    assert len(controller.orders) == 7
    assert controller.count_open_orders == 4
    assert controller.count_closed_orders == 3
    assert controller.count_open_delayed_orders == 2
    assert controller.count_open_ontime_orders == 2


@mock.patch('sinteglas.controller.SinteglasOrderController.now')
def test_confirm_delivery(mock_now, controller):
    mock_now.return_value = datetime.datetime(2015, 12, 25, 12, 22, 11)
    order_params = controller.create_blank_order()
    order_params.estimated_delivery_date = datetime.date(2015, 12, 31)
    controller.save_new_order(order_params)
    controller.load_orders()
    [order] = controller.orders

    controller.confirm_delivery(order)

    [order_from_db] = controller.session.query(Order).all()

    assert order_from_db.delivery_date == datetime.date(2015, 12, 25)


