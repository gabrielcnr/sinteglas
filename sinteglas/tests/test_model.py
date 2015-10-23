import datetime
from sinteglas.model import Order, OrderParams
import mock


@mock.patch('sinteglas.model.Order._now')
def test_order_is_on_time(mock_now):
    mock_now.return_value = datetime.datetime(2015, 10, 20, 10, 10)

    order = Order(
        estimated_delivery_date=datetime.date(2015, 10, 22),
    )

    assert order.status == order.ON_TIME


@mock.patch(
    'sinteglas.model.OrderParams._get_suggested_estimated_delivery_date')
def test_order_params_new(mock_edd):
    mock_edd.return_value = datetime.date(2015, 11, 2)

    order_params = OrderParams.new()
    assert order_params.estimated_delivery_date == datetime.date(2015, 11, 2)


def test_order_params_valid():
    order_params = OrderParams.new()
    assert not order_params.is_valid

    order_params.client = 'foo'

    assert not order_params.is_valid

    order_params.description = 'bar'

    assert order_params.is_valid
