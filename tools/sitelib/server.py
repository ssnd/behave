from flask import Flask, render_template, request
import sys, os

from sklearn.preprocessing import StandardScaler

from sklearn.ensemble import IsolationForest
from sklearn.covariance import EllipticEnvelope
from sklearn import svm
sys.path.append("../../")

from lib.behave import Behave
from lib.keyboard import Keyboard




app = Flask(__name__)



@app.route("/register", methods=['GET', 'POST'])
def register():

	if (request.method== 'GET') :
		return render_template("register.html")

	if (request.method=="POST"):

		data = request.json

		params_arr = []



		for key in sorted(data):

			print key, " : ",  data[key]

			current_key = data[key]

			# print current_key

			behave_instance = Keyboard(data=current_key)

			press_to_press = behave_instance.press_to_press()

			release_to_release = behave_instance.release_to_release()

			dwell = behave_instance.dwell_time()

			flight = behave_instance.flight_time()

			press_to_press_average = behave_instance.average(press_to_press)
			release_to_release_average = behave_instance.average(release_to_release)
			flight_average = behave_instance.average(flight)
			dwell_average = behave_instance.average(dwell)

			params = [press_to_press_average, release_to_release_average, flight_average, dwell_average]
			print params

			params_arr.append(params)



		print '\n\n'
	
		print params_arr

		print params_arr[:4]
		print params_arr[4]
		# normalization
		scaler = StandardScaler().fit(params_arr[:4])

		X = scaler.transform(params_arr[:4])

		# clf = svm.OneClassSVM(nu=.4, kernel="rbf", gamma=0.5, verbose=True)
		# clf = EllipticEnvelope()
		clf = IsolationForest(contamination=0.4, bootstrap=True, max_features=4)

		clf.fit(X)

		print clf.predict(X)

		X_check = scaler.transform([params_arr[4]])


		print clf.predict(X_check)



		return "ok";


@app.route("/login")
def login():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)