from flask import Flask, render_template, request
import sys, os

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

		for key in data:

			current_key = data[key]

			behave_instance = Keyboard(data=current_key)

			press_to_press = behave_instance.press_to_press()

			release_to_release = behave_instance.release_to_release()

			dwell = behave_instance.dwell_time()

			flight = behave_instance.flight_time()

			print release_to_release, press_to_press, flight, dwell








		return "ok";


@app.route("/login")
def login():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)