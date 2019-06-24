from database_setup import Base, Language, FrameWork
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

app = Flask(__name__)

engine = create_engine('sqlite:///frameworksmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Making an API Endpoint (GET Request)
@app.route('/languages/<int:language_id>/frameworks/JSON')
def languageFrameworksJSON(language_id):
    language = session.query(Language).filter_by(id=language_id).one()
    frameworks = session.query(FrameWork).filter_by(
        language_id=language_id).all()
    return jsonify(Frameworks=[i.serialize for i in frameworks])

@app.route('/')
@app.route('/languages/<int:language_id>/')
def languageMenu(language_id):
    language = session.query(Language).filter_by(id=language_id).one()
    frameworks = session.query(FrameWork).filter_by(language_id=language.id)
    return render_template('menu.html', language=language, frameworks=frameworks)

# add a anew framework
@app.route('/languages/<int:language_id>/new/', methods=['GET', 'POST'])
def newFrameWork(language_id):
    if request.method == 'POST':
        framework = FrameWork(
            name=request.form['name'], language_id=language_id)
        session.add(framework)
        session.commit()
        flash("New FrameWork has been added")
        return redirect(url_for('languageMenu', language_id=language_id))
    else:
        return render_template('newFrameWork.html', language_id=language_id)

# edit a framework
@app.route('/languages/<int:language_id>/<int:framework_id>/edit/', methods=['GET', 'POST'])
def editFrameWork(language_id, framework_id):
    editedFramework = session.query(FrameWork).filter_by(id=framework_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedFramework.name = request.form['name']
        session.add(editedFramework)
        session.commit()
        flash("New FrameWork has been Edited")
        return redirect(url_for('languageMenu', language_id=language_id))
    else:
        return render_template('editFramework.html', language_id=language_id, framework_id=framework_id, item=editedFramework)

# delete a framework
@app.route('/languages/<int:language_id>/<int:framework_id>/delete/', methods=['GET', 'POST'])
def deleteFrameWork(language_id, framework_id):
    framework_to_delete = session.query(
        FrameWork).filter_by(id=framework_id).one()
    if request.method == 'POST':
        session.delete(framework_to_delete)
        session.commit()
        flash("A frameWork has been deleted")
        return redirect(url_for('languageMenu', language_id=language_id))
    else:
        return render_template('deleteFramework.html', item=framework_to_delete)


if __name__ == '__main__':
    app.secret_key = 'anaconda' # a big python :D
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
