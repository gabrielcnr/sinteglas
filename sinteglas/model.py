from atom.api import Atom, Str, Typed
import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Order(Base):
    __tablename__ = 'order'

    DELAYED = 'DELAYED'
    ON_TIME = 'ON_TIME'

    id = Column(Integer, primary_key=True)
    client = Column(String(255))
    created_by = Column(String(255))
    description = Column(String(1000))
    created_date = Column(DateTime)
    estimated_delivery_date = Column(Date)
    delivery_date = Column(Date)

    @property
    def status(self):
        if self._now().date() > self.estimated_delivery_date:
            return self.DELAYED
        else:
            return self.ON_TIME

    def _now(self):
        return datetime.datetime.now()


class OrderParams(Atom):
    client = Str()
    description = Str()
    estimated_delivery_date = Typed(datetime.date)


def create_database_session():
    engine = create_engine('sqlite://', echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
