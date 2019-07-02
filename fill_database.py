from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Language, Base, FrameWork, User


db_url = 'postgresql://postgres:anaconda@localhost/frameworks'
engine = create_engine(db_url)

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

# Lang-Python
python = Language(user_id=1, name="Python", icon="devicon-python-plain-wordmark colored")

session.add(python)
session.commit()

unknown = User(name="Unknown", email="no-email")
session.add(unknown)
session.commit()

guido = User(name="Guido Van Rossum", email="guido@python.com")
session.add(guido)
session.commit()
# FW-flask
flask = FrameWork(user_id=1,
                  name="Flask",
                  description="Flask is a microframework for Python based on Werkzeug, Jinja 2 and good intentions. And before you ask: It's BSD licensed!",
                  website="http://flask.pocoo.org/",
                  language=python
                  )

session.add(flask)
session.commit()

# FW-django
django = FrameWork(user_id=1,
                   name="Django",
                   description="Django makes it easier to build better Web apps more quickly and with less code.",
                   website="https://www.djangoproject.com/",
                   language=python,
                   icon="devicon-django-plain colored"
                   )

session.add(django)
session.commit()
# End of python frameworks

# Lang-JavaScript
javascript = Language(user_id=1, name="JavaScript", icon="devicon-javascript-plain colored")

session.add(javascript)
session.commit()

# FW-react
react = FrameWork(user_id=1,
                  name="React",
                  description="A JavaScript library for building user interfaces",
                  website="https://reactjs.org/",
                  language=javascript,
                  icon="devicon-react-original colored"
                  )

session.add(react)
session.commit()


# FW-vuejs
vueJs = FrameWork(user_id=1,
                  name="VueJs",
                  description="The ProgressiveJavaScript Framework",
                  website="https://vuejs.org/",
                  language=javascript,
                  icon="devicon-vuejs-plain colored"
                  )

session.add(vueJs)
session.commit()

# Lang-Ruby
ruby = Language(user_id=1, name="Ruby", icon="devicon-ruby-plain colored")

session.add(ruby)
session.commit()

# FW-ROR
ror = FrameWork(user_id=1,
                name="Ruby on Rails",
                description="Imagine what you could build if you learned Ruby on Rails",
                website="https://rubyonrails.org/",
                language=ruby,
                icon="devicon-rails-plain colored"
                )

session.add(ror)
session.commit()

# FW-Sinatra
sinatra = FrameWork(user_id=1,
                    name="Sinatra",
                    description="Sinatra is a DSL for quickly creating web applications in Ruby with minimal effort",
                    website="http://sinatrarb.com/",
                    language=ruby
                    )

session.add(sinatra)
session.commit()

# Lang-Elixir
elixir = Language(user_id=1, name="Elixir", icon="devicon-erlang-plain colored")

session.add(elixir)
session.commit()


# FW-phoenix
phoenix = FrameWork(user_id=1,
                    name="Phoenix",
                    description="A productive web framework that does not compromise speed or maintainability.",
                    website="https://phoenixframework.org/",
                    language=elixir
                    )

session.add(phoenix)
session.commit()

print("Added FrameWorks to DB")

