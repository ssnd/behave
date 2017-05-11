import sys, json, os, ast

from sklearn.preprocessing import StandardScaler

from sklearn.ensemble import IsolationForest
from sklearn.covariance import EllipticEnvelope
from sklearn import svm

from flask import Flask, request, g, jsonify, session, render_template
app = Flask(__name__)

sys.path.insert(0, os.path.abspath("../../"))
from lib import Behave, Keyboard, Mouse

@app.route("/session", methods=["GET", "POST"])
def continuous():

	data_chunk = ast.literal_eval(request.data)

	keyboard_chunks_value = 3

	mouse_clicks_chunks_value = 3

	mouse_moves_chunks_value = 3

	if data_chunk["type"] == "keyboard" and len([k for k in ast.literal_eval(data_chunk["data"]) if len(k["keyCode"]) == 1]) > 5:
		if not "keyboard" in session:
			session["keyboard"] = []

		keyboard_storage = session["keyboard"]

		key_group = str(data_chunk["data"]) 

		#print request.data, " ---"

		key_instance = Keyboard(data=key_group)

		key_group_params = key_instance.get_keyboard_params().values()

		print "KEYBOARD PARAMETERS: ", key_group_params

		if len(keyboard_storage) > keyboard_chunks_value:

			params_arr = []

			for _session in keyboard_storage:

				behave_instance = Keyboard(data=_session)

				params = behave_instance.get_keyboard_params().values()

				print behave_instance.get_keyboard_params()

				params_arr.append(params)

			scaler = StandardScaler().fit(params_arr)

			# clf = svm.OneClassSVM(nu=.4, kernel="rbf", gamma=0.5, verbose=True)
			# clf = EllipticEnvelope()
			clf = IsolationForest(contamination=0.1, bootstrap=True, max_features=4)

			print params_arr

			X = scaler.transform(params_arr)

			clf.fit(X)

			print key_group_params, " ", type(key_group_params)

			X_check = scaler.transform([key_group_params])

			prediction = clf.predict(X_check)

			print prediction

			if(prediction[0]==-1):
				return jsonify({"status": "INTERRUPT"})

		keyboard_storage.append(key_group)
		print "STORAGE: ", keyboard_storage
		
		session["keyboard"] = keyboard_storage


	if data_chunk["type"] == "mouse_events":
		mouse_event_group = data_chunk["data"]

		mouse_instance = Mouse(data=mouse_event_group)

		mouse_instance_params = mouse_instance.get_mouse_params()

		if not "mouse_events" in session:
			session["mouse_events"] = {}

		mouse_events_storage = session["mouse_events"]



		if len([len(mouse_events_storage[k]) for k in mouse_events_storage]) > 0 and min([len(mouse_events_storage[k]) for k in mouse_events_storage if mouse_instance_params[k] != None]) > mouse_moves_chunks_value:
			
			params_arr = []

			mouse_instance_params_values = [mouse_instance_params[k] for k in mouse_instance_params if mouse_instance_params[k] != None]

			for key in mouse_instance_params:
				if mouse_instance_params[key] != None:
					params_arr.append(mouse_events_storage[key])

			params_arr = [k[:min([len(j) for j in params_arr])] for k in params_arr]

			params_arr = [[j[i] for j in params_arr] for i in range(len(params_arr[0]))]
			
			print mouse_instance_params_values, "----------PARAMS VALUES"

			print params_arr
			
			scaler = StandardScaler().fit(params_arr)

			# clf = svm.OneClassSVM(nu=.4, kernel="rbf", gamma=0.5, verbose=True)
			# clf = EllipticEnvelope()
			clf = IsolationForest(contamination=0.05, bootstrap=True, max_features=len(mouse_instance_params_values))

			X = scaler.transform(params_arr)

			clf.fit(X)

			print mouse_instance_params_values, " ", type(mouse_instance_params_values)

			X_check = scaler.transform([mouse_instance_params_values])

			print X_check

			prediction = clf.predict(X_check)

			print prediction

			if(prediction[0]==-1):
				return jsonify({"status": "INTERRUPT"})

			
		for key in mouse_instance_params:
			if not key in mouse_events_storage:
				mouse_events_storage[key] = []

			if mouse_instance_params[key] != None:
				mouse_events_storage[key].append(mouse_instance_params[key])

		session["mouse_events"] = mouse_events_storage


	return jsonify({"status": "SUCCESS"})

@app.route("/jslib", methods=["GET", "POST"])
def jslib():

	chunks = ast.literal_eval(request.data)

	print "REGISTERED ---" 

	for chunk in chunks:


		data_chunk = ast.literal_eval(chunk)

		keyboard_chunks_value = 4

		if data_chunk["type"] == "keyboard" and len([k for k in data_chunk["data"] if len(k["keyCode"]) == 1]) > 5:
			if not "keyboard" in session:
				session["keyboard"] = []

			keyboard_storage = session["keyboard"]

			key_group = str(data_chunk["data"]) 

			#print request.data, " ---"

			key_instance = Keyboard(data=key_group)

			key_group_params = key_instance.get_keyboard_params().values()

			print "KEYBOARD PARAMETERS: ", key_group_params

			if len(keyboard_storage) > keyboard_chunks_value:

				params_arr = []

				for _session in keyboard_storage:

					behave_instance = Keyboard(data=_session)

					params = behave_instance.get_keyboard_params().values()

					print behave_instance.get_keyboard_params()

					params_arr.append(params)

				scaler = StandardScaler().fit(params_arr)

				# clf = svm.OneClassSVM(nu=.4, kernel="rbf", gamma=0.5, verbose=True)
				# clf = EllipticEnvelope()
				clf = IsolationForest(contamination=0.3, bootstrap=True, max_features=4)

				print params_arr

				X = scaler.transform(params_arr)

				clf.fit(X)

				print key_group_params, " ", type(key_group_params)

				X_check = scaler.transform([key_group_params])

				prediction = clf.predict(X_check)

				print prediction

				if(prediction==-1):
					return jsonify({"status": "INTERRUPT"})

			keyboard_storage.append(key_group)
			
			session["keyboard"] = keyboard_storage

	return jsonify({"status": "SUCCESS"})


@app.route("/register")
def register():
	if request.method=="GET":
		return render_template("register.html")


@app.route("/login")
def login():
	if request.method=="GET":
		return render_template("login.html")


app.secret_key = os.urandom(32)

if __name__ == "__main__":

	app.run(debug=True)