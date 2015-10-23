import datetime
from sinteglas.controller import SinteglasOrderController
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
