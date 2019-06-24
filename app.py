from flask import Flask
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Language, FrameWork

engine = create_engine('sqlite:///frameworksmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/languages/<int:language_id>/')
def languageMeni(language_id):
    language = session.query(Language).filter_by(id = language_id).one()
    frameworks = session.query(FrameWork).filter_by(language_id = language.id)
    output = ''
    for i in frameworks:
        output += i.name
        output += '</br>'
        output += i.description
        output += '</br>'
        output += i.website
        output += '</br>'
        output += '</br>'
    return output

# add a anew framework
@app.route('/languages/<int:language_id>/new/')
def newFrameWork(language_id):
    return "page to create a new framework to the language"

# edit a framework
@app.route('/languages/<int:language_id>/<int:framework_id>/edit/')
def editFrameWork(language_id, framework_id):
    return "let's edit"

# delete a framework
@app.route('/languages/<int:language_id>/<int:framework_id>/delete/')
def deleteFrameWork(language_id, framework_id):
    return "let's delete"



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
