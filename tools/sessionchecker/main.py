import sys, json, os

from sklearn.preprocessing import StandardScaler

from sklearn.ensemble import IsolationForest
from sklearn.covariance import EllipticEnvelope
from sklearn import svm

from flask import Flask, request, g, jsonify, session
app = Flask(__name__)

sys.path.insert(0, os.path.abspath("../../"))
from lib import Behave, Keyboard, Mouse

@app.route("/session", methods=["GET", "POST"])
def keyboard():
	if not "storage" in session:
		session["storage"] = []


	session_storage = session["storage"]

	key_group = str(request.data)

	print key_group

	#print request.data, " ---"

	key_instance = Keyboard(data=key_group)

	key_group_params = key_instance.get_keyboard_params().values()

	print key_group_params

	if len(session_storage) > 2:

		params_arr = []

		for session_ in session_storage:

			behave_instance = Keyboard(data=session_)

			params = behave_instance.get_keyboard_params().values()

			print behave_instance.get_keyboard_params()

			params_arr.append(params)

		scaler = StandardScaler().fit(params_arr)

		# clf = svm.OneClassSVM(nu=.4, kernel="rbf", gamma=0.5, verbose=True)
		# clf = EllipticEnvelope()
		clf = IsolationForest(contamination=0.15, bootstrap=True, max_features=4)

		X = scaler.transform(params_arr)

		clf.fit(X)

		print key_group_params, " ", type(key_group_params)

		X_check = scaler.transform([key_group_params])

		print X_check

		prediction = clf.predict(X_check)

		print prediction

		if(prediction[0]==-1):
			return jsonify({"status": "INTERRUPT"})



	session_storage.append(key_group)

	session["storage"] = session_storage

	return jsonify({"status": "SUCCESS"})


@app.route("/mousetest", methods=['GET','POST'])
def mouse_test():
	print request.data;
	return "1"



app.secret_key = os.urandom(32)

if __name__ == "__main__":

	app.run(debug=True)