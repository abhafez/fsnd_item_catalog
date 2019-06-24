from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Language, Base, FrameWork

engine = create_engine('sqlite:///frameworksmenu.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

# Lang-Python
python = Language(name="Python")

session.add(python)
session.commit()

# FW-flask
flask = FrameWork(name="Flask",
                  description="Flask is a microframework for Python based on Werkzeug, Jinja 2 and good intentions. And before you ask: It's BSD licensed!",
                  website="http://flask.pocoo.org/",
                  language=python
                  )

session.add(flask)
session.commit()

# FW-django
django = FrameWork(name="Django",
                   description="Django makes it easier to build better Web apps more quickly and with less code.",
                   website="https://www.djangoproject.com/",
                   language=python
                   )

session.add(django)
session.commit()
# End of python frameworks

# Lang-JavaScript
javascript = Language(name="JavaScript")

session.add(javascript)
session.commit()

# FW-react
react = FrameWork(name="React",
                  description="A JavaScript library for building user interfaces",
                  website="https://reactjs.org/",
                  language=javascript
                  )

session.add(react)
session.commit()

# FW-angular
angular = FrameWork(name="Angular",
                    description="Build features quickly with simple, declarative templates. Extend the template language with your own components and use a wide array of existing components. Get immediate Angular-specific help and feedback with nearly every IDE and editor. All this comes together so you can focus on building amazing apps rather than trying to make the code work.",
                    website="https://angular.io/",
                    language=javascript
                    )

session.add(angular)
session.commit()

# FW-vuejs
vueJs = FrameWork(name="VueJs",
                  description="The ProgressiveJavaScript Framework",
                  website="https://vuejs.org/",
                  language=javascript
                  )

session.add(vueJs)
session.commit()

# Lang-Ruby
ruby = Language(name="Ruby")

session.add(ruby)
session.commit()

# FW-ROR
ror = FrameWork(name="Ruby on Rails",
                description="Imagine what you could build if you learned Ruby on Rails…",
                website="https://rubyonrails.org/",
                language=ruby
                )

session.add(ror)
session.commit()

# FW-Sinatra
sinatra = FrameWork(name="Sinatra",
                description="Sinatra is a DSL for quickly creating web applications in Ruby with minimal effort",
                website="http://sinatrarb.com/",
                language=ruby
                )

session.add(sinatra)
session.commit()

# Lang-Elixir
elixir = Language(name="Elixir")

session.add(elixir)
session.commit()


# FW-phoenix
phoenix = FrameWork(name="Phoenix",
                description="A productive web framework that does not compromise speed or maintainability.",
                website="https://phoenixframework.org/",
                language=elixir
                )

session.add(phoenix)
session.commit()

print("Added FrameWorks to DB")
