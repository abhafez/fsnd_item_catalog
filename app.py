from database_setup import Base, Language, FrameWork, User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
from flask import session as login_session
import json
import random
import string
app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Frameworks List Application"

engine = create_engine('sqlite:///frameworksmenuwithusersandicons.db', connect_args={'check_same_thread': False})
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        print('catch it')
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        print('catch it after authflow')
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print("done!")
    return output


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print('In gdisconnect access token is %s', access_token)
    print('User name is: ')
    print(login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result is ')
    print(result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# Making an API Endpoint (GET Request)
@app.route('/languages/<int:language_id>/framework/JSON')
def languageFrameworksJSON(language_id):
    frameworks = session.query(FrameWork).filter_by(
        language_id=language_id).all()
    return jsonify(Frameworks=[i.serialize for i in frameworks])


@app.route('/languages/<int:language_id>/framework/<int:framework_id>/JSON')
def FrameworkJSON(language_id, framework_id):
    framework = session.query(FrameWork).filter_by(id=framework_id).one()
    return jsonify(Framework=[framework.serialize])


@app.route('/')
def hello():
    return redirect("/languages/", code=302)

@app.route('/languages/')
def languageMenu():
    languages = session.query(Language).order_by((Language.name))
    # frameworks = session.query(FrameWork).filter_by(language_id=language.id)
    return render_template('programmingLanguagesMenu.html', languages=languages)

# add a anew framework
@app.route('/languages/<int:language_id>/new/', methods=['GET', 'POST'])
def newFrameWork(language_id):
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        framework = FrameWork(
            name=request.form['name'], language_id=language_id, user_id=login_session['user_id'])
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
    if 'username' not in login_session:
        return redirect('/login')
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
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        session.delete(framework_to_delete)
        session.commit()
        flash("A frameWork has been deleted")
        return redirect(url_for('languageMenu', language_id=language_id))
    else:
        return render_template('deleteFramework.html', item=framework_to_delete)


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


if __name__ == '__main__':
    app.secret_key = 'anaconda'  # a big python :D
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
