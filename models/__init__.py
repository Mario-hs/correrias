# from app.models import db
# from sqlalchemy import Boolean, create_engine, ForeignKey
# from sqlalchemy import Column, Date, Integer, String, Float
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker


# engine = create_engine(f"sqlite:///./storage.sqlite", echo=True)
# db = declarative_base()

# # Declaracao das classes

# class Station(db):

#     __tablename__ = "station"

#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     password = Column(String, nullable=False)
#     email = Column(String, nullable=False)
#     cnpj = Column(String, nullable=False)

#     def __repr__(self, name, password):
#         self.name = name
#         self.password = password

#         return f"<Station {self.name}>"


# class Package(db):

#     __tablename__ = "package"

#     id = Column(Integer, primary_key=True)
#     products_id = Column(Integer, nullable=False)
#     products_name = Column(String, nullable=False)
#     weight = Column(Integer, nullable=False)
#     destiny_id = Column(String, ForeignKey("station.id"))
#     status_transaction = Column(Boolean, nullable=False)
#     sender_cpf = Column(String, nullable=False)
#     sender_name = Column(String, nullable=False)

#     def __init__(self, products_name, weight, destiny_id, status_transaction, sender_cpf, sender_name):
#         self.products_name = products_name
#         self.weight = weight
#         self.destiny_id = destiny_id
#         self.status_transaction = status_transaction
#         self.sender_cpf = sender_cpf
#         self.sender_name = sender_name

#         return f"<Package {self.id}>"



# class Transaction(db):

#     __tablename__ = "transaction"

#     id = Column(Integer, primary_key=True)
#     source_id = Column(String, ForeignKey("station.id"))
#     package_id = Column(String, ForeignKey("package.id"))


# # fim da declaracao

# db.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)
# session = Session()