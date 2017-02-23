from flask import request, render_template, redirect, jsonify
from server import db, app, login_manager
from models import User, DataChunk, Collect
from flask_login import login_user, logout_user, current_user, login_required
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.datasets.supervised import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork
import hashlib
import os, sys
from blinker import signal
import json
import base64

# todo: fix
sys.path.insert(0, os.path.abspath("../../"))
from lib.behave import Behave

net = False
min_max = False


send_data = signal("send-data")


@send_data.connect
# @app.before_first_request
def init_neural_net( *args ):

	global net;
	global min_max;

	print "preparing network"

	# number of users
	users = User.query.all()

	user_count = len(users)

	training_data = []

	for user_index in range(len(users)):

		user = users[user_index]

		for data_chunk in user.datachunks:

			data = data_chunk.get_json_data()

			instance = Behave(data=data)

			params = instance.get_all_params()

			prepared_dict = {
				"data" : params,
				"response" : user_index
			}

			# print prepared_dict

			training_data.append(prepared_dict)

	normalized_data = Behave.normalize_training_data(training_data)

	min_max = normalized_data['min_max']

	ds = SupervisedDataSet(3, user_count)

	for index in range(len(normalized_data['responses'])):

		input = normalized_data['data'][index]

		output = normalized_data['responses'][index]
		# print (input, output)
		ds.addSample(input, output)


	net = buildNetwork(3,(3+user_count)*2,user_count)

	trainer = BackpropTrainer(net, learningrate = 0.01, momentum = 0.99)

	trainer.trainOnDataset(ds, 1000)

	trainer.testOnData()

	print min_max


	print "network ready"



@login_manager.user_loader
def load_user(id):

	return User.query.get(int(id))

@login_manager.request_loader
def load_user_from_request(request):

	# next, try to login using Basic Auth
	api_key = request.headers.get('Authorization')

	if api_key:

		user = User.verify_auth_token(api_key)

		if user:
			return user
	
	return None


@app.teardown_appcontext
def shutdown_session(exception=None):

	db.session.remove()

@app.route("/users")
def users():
	data = Collect.query.all()
	cols = ['id', 'dataChunk1','mouseDataChunk1', "name" , "lastname"]
	result = [{col: getattr(d, col) for col in cols} for d in data]
	return jsonify(result)

@app.route("/", methods=["GET"])
# @login_required
def home():

	send_data.send("1")

	# print net.activate((0.0, 1.0, 0.0))

	return "ok"


@app.route("/login", methods=["POST", "GET"])
def login():

	if request.method=="GET":
		return render_template("login.html")

	username = request.json['username']
	password = request.json['password']


	pass_hash = hashlib.sha512(password).hexdigest()

	registered_user = User.query.filter_by(username=username, password=pass_hash).first()

	if registered_user is None:
		return jsonify({
			"response" : "error",
			"error" : "Check the username or password",
			"token" : "",

		})

	login_user(registered_user, remember=True)

	return jsonify({
		"status" : "ok",
		"token" : registered_user.generate_auth_token(),
		"user_id" : registered_user.id,
		"error" : "",
	})


@app.route("/logout", methods=["POST", "GET"])
def logout():

	logout_user()

	return jsonify({
		"status" : "ok"
	})


@app.route("/register", methods=["GET", "POST"])
def register():

	if request.method=="GET":
		return render_template("register.html")


	username	= request.json['username']
	password	= request.json['password']
	email		= request.json['email']
	pass_hash 	= hashlib.sha512(password).hexdigest()

	u = User(
		username,
		email,
		pass_hash
	)

	db.session.add(u)
	db.session.commit()

	return jsonify({
		"status" : "ok"
	})


@app.route("/collect", methods=["GET", "POST"])
def collect():

	email			= request.json['email']
	name			= request.json['name']
	lastname		= request.json['lastname']
	age				= request.json['age']
	gender			= request.json['gender']
	dataChunk1		= request.json['dataChunk1']
	dataChunk2		= request.json['dataChunk2']
	dataChunk3		= request.json['dataChunk3']
	dataChunk4		= request.json['dataChunk4']
	mouseDataChunk1	= request.json['mouseDataChunk1']
	mouseDataChunk2	= request.json['mouseDataChunk2']
	mouseDataChunk3	= request.json['mouseDataChunk3']
	mouseDataChunk4	= request.json['mouseDataChunk4']

	c = Collect(
		email,
		name,
		lastname,
		age,
		gender,
		dataChunk1,
		dataChunk2,
		dataChunk3,
		dataChunk4,
		mouseDataChunk1,
		mouseDataChunk2,
		mouseDataChunk3,
		mouseDataChunk4
	)

	db.session.add(c)
	db.session.commit()

	return jsonify({
		"status" : "ok"
	})

@app.route("/train", methods=["GET", "POST"])
@login_required
def add_data_chunk():

	if request.method=="GET":
		return render_template("add_data_chunk.html")

	data = str(request.json['data'])

	d = DataChunk(current_user.id, data)

	print current_user

	db.session.add(d)

	db.session.commit()

	print current_user.datachunks

	return "ok"

@app.route("/test_net", methods=['GET', 'POST'])
def test_net():

	# d = [{"timestamp": 1481038256404, "key_duration": 80, "keycode": 16}, {"timestamp": 1481038256435, "key_duration": 110, "keycode": 65}, {"timestamp": 1481038256635, "key_duration": 103, "keycode": 70}, {"timestamp": 1481038256833, "key_duration": 22, "keycode": 84}, {"timestamp": 1481038256942, "key_duration": 87, "keycode": 69}, {"timestamp": 1481038258363, "key_duration": 78, "keycode": 82}, {"timestamp": 1481038258497, "key_duration": 45, "keycode": 188}, {"timestamp": 1481038258554, "key_duration": 102, "keycode": 32}, {"timestamp": 1481038258848, "key_duration": 64, "keycode": 8}, {"timestamp": 1481038258970, "key_duration": 2, "keycode": 8}, {"timestamp": 1481038259039, "key_duration": 71, "keycode": 32}, {"timestamp": 1481038259167, "key_duration": 19, "keycode": 65}, {"timestamp": 1481038259218, "key_duration": 70, "keycode": 32}, {"timestamp": 1481038259858, "key_duration": 21, "keycode": 87}, {"timestamp": 1481038259915, "key_duration": 1, "keycode": 72}, {"timestamp": 1481038259983, "key_duration": 69, "keycode": 73}, {"timestamp": 1481038260015, "key_duration": 32, "keycode": 76}, {"timestamp": 1481038260076, "key_duration": 93, "keycode": 69}, {"timestamp": 1481038260259, "key_duration": 38, "keycode": 188}, {"timestamp": 1481038260339, "key_duration": 118, "keycode": 32}, {"timestamp": 1481038260582, "key_duration": 31, "keycode": 70}, {"timestamp": 1481038260668, "key_duration": 48, "keycode": 73}, {"timestamp": 1481038260731, "key_duration": 111, "keycode": 78}, {"timestamp": 1481038260887, "key_duration": 126, "keycode": 68}, {"timestamp": 1481038261022, "key_duration": 56, "keycode": 73}, {"timestamp": 1481038261077, "key_duration": 111, "keycode": 78}, {"timestamp": 1481038261189, "key_duration": 1, "keycode": 71}, {"timestamp": 1481038261290, "key_duration": 102, "keycode": 32}, {"timestamp": 1481038261508, "key_duration": 46, "keycode": 84}, {"timestamp": 1481038261556, "key_duration": 94, "keycode": 72}, {"timestamp": 1481038261695, "key_duration": 2, "keycode": 65}, {"timestamp": 1481038261750, "key_duration": 57, "keycode": 84}, {"timestamp": 1481038261776, "key_duration": 83, "keycode": 32}, {"timestamp": 1481038262100, "key_duration": 1, "keycode": 78}, {"timestamp": 1481038262171, "key_duration": 72, "keycode": 79}, {"timestamp": 1481038262325, "key_duration": 77, "keycode": 72}, {"timestamp": 1481038262326, "key_duration": 78, "keycode": 84}, {"timestamp": 1481038262995, "key_duration": 111, "keycode": 78}, {"timestamp": 1481038263258, "key_duration": 79, "keycode": 8}, {"timestamp": 1481038263494, "key_duration": 55, "keycode": 73}, {"timestamp": 1481038263531, "key_duration": 15, "keycode": 78}, {"timestamp": 1481038263624, "key_duration": 29, "keycode": 71}, {"timestamp": 1481038263690, "key_duration": 95, "keycode": 32}, {"timestamp": 1481038263918, "key_duration": 47, "keycode": 77}, {"timestamp": 1481038263980, "key_duration": 61, "keycode": 79}, {"timestamp": 1481038264008, "key_duration": 26, "keycode": 82}, {"timestamp": 1481038264051, "key_duration": 2, "keycode": 69}, {"timestamp": 1481038264111, "key_duration": 62, "keycode": 32}, {"timestamp": 1481038264284, "key_duration": 64, "keycode": 72}, {"timestamp": 1481038264474, "key_duration": 47, "keycode": 65}, {"timestamp": 1481038264497, "key_duration": 70, "keycode": 80}, {"timestamp": 1481038264654, "key_duration": 26, "keycode": 80}, {"timestamp": 1481038264722, "key_duration": 94, "keycode": 69}, {"timestamp": 1481038264960, "key_duration": 143, "keycode": 68}, {"timestamp": 1481038265249, "key_duration": 70, "keycode": 8}, {"timestamp": 1481038265419, "key_duration": 15, "keycode": 78}, {"timestamp": 1481038265513, "key_duration": 109, "keycode": 69}, {"timestamp": 1481038265583, "key_duration": 47, "keycode": 68}, {"timestamp": 1481038265854, "key_duration": 30, "keycode": 188}, {"timestamp": 1481038265918, "key_duration": 94, "keycode": 32}, {"timestamp": 1481038266113, "key_duration": 79, "keycode": 83}, {"timestamp": 1481038266255, "key_duration": 55, "keycode": 69}, {"timestamp": 1481038266584, "key_duration": 111, "keycode": 8}, {"timestamp": 1481038266770, "key_duration": 16, "keycode": 72}, {"timestamp": 1481038266832, "key_duration": 78, "keycode": 69}, {"timestamp": 1481038267001, "key_duration": 111, "keycode": 32}, {"timestamp": 1481038267148, "key_duration": 87, "keycode": 68}, {"timestamp": 1481038267195, "key_duration": 46, "keycode": 69}, {"timestamp": 1481038267373, "key_duration": 4, "keycode": 67}, {"timestamp": 1481038267439, "key_duration": 70, "keycode": 73}, {"timestamp": 1481038267570, "key_duration": 23, "keycode": 68}, {"timestamp": 1481038267672, "key_duration": 23, "keycode": 69}, {"timestamp": 1481038267751, "key_duration": 102, "keycode": 68}, {"timestamp": 1481038267856, "key_duration": 79, "keycode": 32}, {"timestamp": 1481038267996, "key_duration": 40, "keycode": 79}, {"timestamp": 1481038268073, "key_duration": 21, "keycode": 78}, {"timestamp": 1481038268154, "key_duration": 102, "keycode": 32}, {"timestamp": 1481038268268, "key_duration": 53, "keycode": 71}, {"timestamp": 1481038268331, "key_duration": 30, "keycode": 79}, {"timestamp": 1481038268393, "key_duration": 32, "keycode": 73}, {"timestamp": 1481038268462, "key_duration": 101, "keycode": 78}, {"timestamp": 1481038268561, "key_duration": 2, "keycode": 71}, {"timestamp": 1481038268630, "key_duration": 71, "keycode": 32}, {"timestamp": 1481038269297, "key_duration": 16, "keycode": 73}, {"timestamp": 1481038269373, "key_duration": 22, "keycode": 78}, {"timestamp": 1481038269477, "key_duration": 2, "keycode": 84}, {"timestamp": 1481038269562, "key_duration": 21, "keycode": 79}, {"timestamp": 1481038269619, "key_duration": 78, "keycode": 32}, {"timestamp": 1481038269740, "key_duration": 22, "keycode": 84}, {"timestamp": 1481038269810, "key_duration": 92, "keycode": 72}]
	data = request.json['data']

	instance = Behave(data=data)

	print instance.get_all_params()

	nd = instance.normalize_data(min_max)

	print nd

	response = net.activate(nd)

	result = None

	for i in range(len(response)):
		if response[i] > 0.5: result = i

	print result

	print response 
	user = User.query.all()[result]

	return jsonify({
		"error": "",
		"response" :  {
			"user" : {
				"id": user.id,
				"name" : user.username
			},
			"probability" : str(response[result]*100)
		}
	})