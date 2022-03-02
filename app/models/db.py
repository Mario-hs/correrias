# from app import db
from sqlalchemy import Boolean, create_engine, ForeignKey, event
from sqlalchemy import Column, Integer, String
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
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

    __tablename__ = "station"

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

class Package(db):

    __tablename__ = "package"

    id = Column(Integer, primary_key=True, autoincrement=True)
    weight = Column(String, nullable=False)
    sender_cpf = Column(String, nullable=False)
    sender_name = Column(String, nullable=False)
class Transaction(db):

    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True, autoincrement=True)
    status_transaction = Column(Boolean, nullable=False)
    source_id = Column(Integer, ForeignKey("station.id"))
    destiny_id = Column(Integer, ForeignKey("station.id"))
    package_id = Column(String, ForeignKey("package.id"))

    def __init__(self, source_id, destiny_id):
        self.source_id
        self.destiny_id

# fim da declaracao

