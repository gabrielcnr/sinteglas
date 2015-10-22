import getpass
from atom.api import *
import datetime
from sinteglas.model import Order, OrderParams

class SinteglasOrderController(Atom):

    session = Value()

    def save_new_order(self, order_params):
        new_order = Order(
            created_date=self.now(),
            created_by=self.get_user(),
            client=order_params.client,
            description=order_params.description,
            estimated_delivery_date=order_params.estimated_delivery_date,
        )
        self.session.add(new_order)
        self.session.commit()
        return new_order

    def create_blank_order(self):
        return OrderParams()

    def get_user(self):
        return getpass.getuser()

    def now(self):
        return datetime.datetime.now()

