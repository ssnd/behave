from server import db
import json
import ast
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from server import app


class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), unique=True)
	password=db.Column(db.String(128), unique=True)
	email = db.Column(db.String(120), unique=True)
	datachunks = db.relationship("DataChunk")

	def __init__(self, username=None, email=None, password=None):
		self.username = username
		self.email = email
		self.password = password

	def is_authenticated(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)

	def is_active(self):
		return True

	def __repr__(self):
		return '<User %r>' % (self.username)

	def generate_auth_token(self):
		s = Serializer(app.config['SECRET_KEY'])
		return s.dumps({'id' : self.id})

	@staticmethod
	def verify_auth_token(token):
		s = Serializer(app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except SignatureExpired:
			return None
		except BadSignature:
			return None
		user = User.query.get(data['id'])
		return user

class DataChunk(db.Model):
	__tablename__ = "datachunks"
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
	data = db.Column(db.String(6000), unique=True)

	def __init__(self, user_id=None, data=None):
		self.user_id = user_id
		self.data = data

	def get_json_data(self):
		return ast.literal_eval(self.data)

