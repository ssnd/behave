from flask import request, render_template, redirect
from server import db, app, login_manager
from models import User, DataChunk
from flask_login import login_user, logout_user, current_user, login_required
import hashlib
import os, sys
from blinker import signal
from pybrain.datasets.supervised import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer

# todo: fix
sys.path.insert(0, os.path.abspath("../../"))
from lib.behave import Behave


send_data = signal("send-data")


@send_data.connect
@app.before_first_request
def init_neural_net( *args ):

	# number of users
	users = User.query.all()

	user_count = len(users)

	print user_count
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

			training_data.append(prepared_dict)

	normalized_data = Behave.normalize_training_data(training_data)

	ds = SupervisedDataSet(3, user_count)

	for index in range(len(normalized_data['responses'])):

		input = normalized_data['data'][index]

		output = normalized_data['responses'][index]

		ds.addSample(input, output)


	net = buildNetwork(3,(3+user_count)*2,user_count)

	trainer = BackpropTrainer(net, learningrate = 0.01, momentum = 0.99)

	trainer.trainOnDataset(ds, 1000)

	trainer.testOnData()





@login_manager.user_loader
def load_user(id):

	return User.query.get(int(id))


@app.teardown_appcontext
def shutdown_session(exception=None):

	db.session.remove()


@app.route("/", methods=["GET"])
@login_required
def home():

	send_data.send("1")

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
		return "!ok"

	login_user(registered_user)

	return "ok"


@app.route("/logout", methods=["POST", "GET"])
def logout():

	logout_user()

	return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():

	if request.method=="GET":
		return render_template("register.html")


	username	= request.form['username']
	password	= request.form['password']
	email		= request.form['email']
	pass_hash 	= hashlib.sha512(password).hexdigest()

	u = User(
		username,
		email,
		pass_hash
	)

	db.session.add(u)
	db.session.commit()

	return redirect("/login")


@app.route("/train", methods=["GET", "POST"])
@login_required
def add_data_chunk():

	if request.method=="GET":
		return render_template("add_data_chunk.html")

	data = request.form['data']

	d = DataChunk(current_user.id, data)

	db.session.add(d)

	db.session.commit()

	return "ok"