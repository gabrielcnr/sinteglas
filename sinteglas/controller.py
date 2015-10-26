import getpass
from atom.api import *
import datetime
from sinteglas.model import Order, OrderParams


class SinteglasOrderController(Atom):
    session = Value()

    orders = List()

    show_closed = Bool()

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

    def conclude_order(self, order):
        order.delivery_date = self.now().date()
        self.session.add(order)
        self.session.commit()

    def delete_order(self, order):
        self.session.delete(order)
        self.session.commit()

    def load_orders(self):
        query = self.session.query(Order)
        self.orders = query.all()


class DemoSinteglasOrderController(SinteglasOrderController):

    def populate_demo_database(self):
        # 2 orders delayed
        self.mk_order(client='Batman', description='2 chapa',
                  estimated_delivery_date=self.mk_date(-1),
                  created_date=self.mk_date(-11),
                  created_by='Seu Fabio')
        self.mk_order(client='Spiderman', description='1 chapa',
                  estimated_delivery_date=self.mk_date(-3),
                  created_date=self.mk_date(-8),
                  created_by='Du Fiasco')
        # 2 orders on time
        self.mk_order(client='IronMan', description='100 mascara',
                  estimated_delivery_date=self.mk_date(+2),
                  created_date=self.mk_date(-5),
                  created_by='Seu Fabio')
        self.mk_order(client='Dilma', description='1 rola x-large',
                  estimated_delivery_date=self.mk_date(+7),
                  created_date=self.mk_date(-6),
                  created_by='Du Fiasco')
        # 2 orders closed on time
        self.mk_order(client='IronMan', description='20 mascara',
                  estimated_delivery_date=self.mk_date(-7),
                  delivery_date=self.mk_date(-9),
                  created_date=self.mk_date(-15),
                  created_by='Estenio Cavalari')
        self.mk_order(client='Batman', description='125 Batchapacrilica',
                  estimated_delivery_date=self.mk_date(+1),
                  delivery_date=self.mk_date(-1),
                  created_date=self.mk_date(-6),
                  created_by='Du Fiasco')
        # 2 orders closed delayed
        self.mk_order(client='Dilma', description='240 algemas acrilicas',
                  estimated_delivery_date=self.mk_date(-3),
                  delivery_date=self.mk_date(-1),
                  created_date=self.mk_date(-16),
                  created_by='Du Fiasco')

        self.session.commit()

    def mk_date(self, delta_days):
        return self.now().date() + datetime.timedelta(days=delta_days)

    def mk_order(self, **kwargs):
        o = Order(**kwargs)
        self.session.add(o)

