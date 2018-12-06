from flask import Flask 
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from flaskext.markdown import Markdown
from flask_pagedown import PageDown

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

moment = Moment(app)

md = Markdown(app, output_format = 'html')
pagedown = PageDown(app)

login = LoginManager(app)
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'

# from app.errors import bp as errors_bp
# app.register_blueprint(errors_bp)
from app.auth import bp as auth_bp
app.register_blueprint(auth_bp, url_prefix = '/auth')

from app.articles import bp as articles_bp
app.register_blueprint(articles_bp, url_prefix = '/articles')

from app import routes, models ,errors

