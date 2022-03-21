# from app import db
from sqlalchemy import Boolean, create_engine, ForeignKey, event
from sqlalchemy import Column, Integer, String
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from app import login_manager

import contextlib

engine = create_engine(f"sqlite:///./storage.sqlite", echo=True)
db = declarative_base()

db.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

@contextlib.contextmanager
def transaction(connection):
    if not connection.in_transaction():
        with connection.begin():
            yield connection
    else:
        yield connection


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

@login_manager.user_loader
def load_user(user_id):
    return session.query(Station).get(user_id)

# Declaracao das classes
class Station(db):

    __tablename__ = "stations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)
    cnpj = Column(String, nullable=False)

    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False
    
    def get_id(Station):
        return str(Station.id)

    # def __repr__(self, name):
    #     self.name = name
    #     return f"<Station {self.name}>"

class Transaction(db):

    __tablename__ = "transactions"

    id_trans = Column(Integer, primary_key=True, autoincrement=True)
    status_transaction = Column(Integer, nullable=False)
    source_id = Column(Integer, ForeignKey("stations.id"), nullable=False)
    destiny_id = Column(Integer, ForeignKey("stations.id"), nullable=False)
    package_id = Column(Integer, ForeignKey("packages.id_pack"))
    package = relationship('Package')
    # trans = relationship(Package, backref="package")
    
class Package(db):

    __tablename__ = "packages"

    id_pack = Column(Integer, primary_key=True, autoincrement=True)
    id_tracking = Column(String, nullable=False)
    weight = Column(String, nullable=False)
    sender_cpf = Column(String, nullable=False)
    sender_name = Column(String, nullable=False)
    sender_email = Column(String, nullable=False)
    transaction = relationship(Transaction, backref="packages")


# fim da declaracao

db.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()