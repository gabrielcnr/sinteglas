import datetime
from sinteglas.controller import SinteglasOrderController
from sinteglas.model import create_database_session, Order
import mock


@mock.patch('sinteglas.controller.SinteglasOrderController.now')
@mock.patch('sinteglas.controller.SinteglasOrderController.get_user')
def test_create_order(mock_get_user, mock_now):
    mock_get_user.return_value = 'edu.fiasco'
    mock_now.return_value = datetime.datetime(2015, 10, 20, 15, 30)

    session = create_database_session()
    controller = SinteglasOrderController(session=session)

    order_params = controller.create_blank_order()
    order_params.client = 'Rodrigo Vila'
    order_params.description = '20 chapa acrilica verde limao'
    order_params.estimated_delivery_date = datetime.date(2015, 10, 27)

    controller.save_new_order(order_params)

    [order] = session.query(Order).all()

    assert order.client == 'Rodrigo Vila'
    assert order.description == '20 chapa acrilica verde limao'
    assert order.created_by == 'edu.fiasco'
    assert order.created_date == datetime.datetime(2015, 10, 20, 15, 30)
    assert order.estimated_delivery_date == datetime.date(2015, 10, 27)
