import datetime
from sinteglas.model import Order
import mock


@mock.patch('sinteglas.model.Order._now')
def test_order_is_on_time(mock_now):
    mock_now.return_value = datetime.datetime(2015, 10, 20, 10, 10)

    order = Order(
        estimated_delivery_date=datetime.date(2015, 10, 22),
    )

    assert order.status == order.ON_TIME
