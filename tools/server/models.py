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
	password=db.Column(db.String(128), unique=False)
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

class Collect(db.Model):
	__tablename__ = "collect"
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(120), unique=False)
	name = db.Column(db.String(120), unique=False)
	lastname = db.Column(db.String(120), unique=False)
	age = db.Column(db.Integer, unique=False)
	gender = db.Column(db.String(100), unique=False)
	dataChunk1 = db.Column(db.String(6000), unique=False)
	dataChunk2 = db.Column(db.String(6000), unique=False)
	dataChunk3 = db.Column(db.String(6000), unique=False)
	dataChunk4 = db.Column(db.String(6000), unique=False)
	mouseDataChunk1 = db.Column(db.String(8000), unique=False)
	mouseDataChunk2 = db.Column(db.String(8000), unique=False)
	mouseDataChunk3 = db.Column(db.String(8000), unique=False)
	mouseDataChunk4 = db.Column(db.String(8000), unique=False)

	def __init__(self, email=None, name=None, lastname=None, age=None, gender=None, dataChunk1=None, dataChunk2=None, dataChunk3=None, dataChunk4=None, mouseDataChunk1=None, mouseDataChunk2=None, mouseDataChunk3=None, mouseDataChunk4=None):
		self.email = email
		self.name = name
		self.lastname = lastname
		self.age = age
		self.gender = gender
		self.dataChunk1 = dataChunk1
		self.dataChunk2 = dataChunk2
		self.dataChunk3 = dataChunk3
		self.dataChunk4 = dataChunk4
		self.mouseDataChunk1 = mouseDataChunk1
		self.mouseDataChunk2 = mouseDataChunk2
		self.mouseDataChunk3 = mouseDataChunk3
		self.mouseDataChunk4 = mouseDataChunk4

	def get_json_data(self, jsonString=None):
		return ast.literal_eval(jsonString)