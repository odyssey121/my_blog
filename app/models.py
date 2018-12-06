from app import db
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from app import login # and for @user_loader decorations
from hashlib import md5
#Because Flask-Login knows nothing about databases,
#it needs the application's help in loading a user.
#For that reason, the extension expects that the application will
#configure a user loader function, 
#that can be called to load a user given the ID.
@login.user_loader
def load_user(id):
	return User.query.get(int(id))

class Comment(db.Model):
	__tablename__ = 'comments'
	id = db.Column(db.Integer, primary_key = True)
	body = db.Column(db.Text)
	body_html = db.Column(db.Text)
	timestamp = db.Column(db.DateTime, index = True, default = datetime.utcnow)
	author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	author_name = db.Column(db.String(64))
	author_email = db.Column(db.String(64))
	notify = db.Column(db.Boolean, default = True)
	approved = db.Column(db.Boolean, default = False)
	article_id = db.Column(db.Boolean, db.ForeignKey('articles.id'))

class Article(db.Model):
	__tablename__ = 'articles'
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(128), nullable = False)
	description = db.Column(db.Text)
	slides = db.Column(db.Text())
	video = db.Column(db.Text())
	venue = db.Column(db.String(128))
	venue_url = db.Column(db.String(128))
	date = db.Column(db.DateTime())
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	comments = db.relationship('Сomment', lazy = 'dynamic', backref = 'article')

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(64), index = True, unique = True)
	email = db.Column(db.String(120), index = True, unique = True)
	password_hash = db.Column(db.String(128))
	about_me = db.Column(db.String(180))
	last_seen = db.Column(db.DateTime, default = datetime.utcnow)
	articles = db.relationship('Article', backref = 'author', lazy = 'dynamic')
	comments = db.relationship('Comment', backref = 'author', lazy = 'dynamic')


	def avatar(self, size):
		digest = md5(str(self.email).lower().encode('utf-8')).hexdigest()
		return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
			digest, size)

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password_hash(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return '<User {} id {} >'.format(self.username, self.id)