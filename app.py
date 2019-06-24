from flask import Flask

from database_setup import Base, Language, FrameWork
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///frameworksmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

session = DBSession()
app = Flask(__name__)

@app.route('/')
def greeting_all():
    return("Hello World")


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
