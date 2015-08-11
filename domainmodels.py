from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Domains(Base):
    __tablename__ = 'domains'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    domain = Column(String(250), nullable=False)
    country = Column(String)
    city = Column(String)
    updated_date = Column(Integer)
    expiration_date = Column(Integer)
    registrar = Column(String)


# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///domainDB.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)

# Need to add default data (just one row for now)