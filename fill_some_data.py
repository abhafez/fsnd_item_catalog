from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Language, Base, FrameWork, User


db_url = 'postgresql://postgres:anaconda@localhost/frameworks'
engine = create_engine(db_url)

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()


guido = User(name="Guido Van Rossum", email="guido@python.com")
session.add(guido)
session.commit()

print("Added FrameWorks to DB")

