# Test server that receives post data and saves it to files
#
#
# IMPORTANT:
# a required argument when starting the script is the path where the files should be saved 
#
#
#

from flask import Flask, request
import os
import sys
from flask_cors import CORS, cross_origin
import pybrain
from pybrain.datasets import *
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer

# snippet to import the library without relative routes
sys.path.insert(0, os.path.abspath("../.."))

from behave.lib import Behave


FILES_PATH = "../data/user_typing_info"


app = Flask(__name__)
CORS(app)


def encode_dict(d, codec='utf8'):

	ks = d.keys()

	for k in ks:

		val = d.pop(k)

		if isinstance(val, unicode):

			val = val.encode(codec)

		elif isinstance(val, dict):

			val = encode_dict(val, codec)

		if isinstance(k, unicode):

			k = k.encode(codec)

		d[k] = val

	return d


@app.route("/", methods=["POST"])
def home():

	files = os.listdir(FILES_PATH)

	json_request = encode_dict(request.json)

	max_index = 0

	for file in files:

		try: file_int = int(file)
		except ValueError: continue

		max_index = max(max_index, file_int)


	max_index += 1 

	file = open(FILES_PATH + "/" + str(max_index), "w")

	file.write(str(json_request))

	return "file is saved"


@app.route("/verify", methods=['POST'])
def verify():
	# json_request = encode_dict(request.json)

	# json_request = [{'timestamp': 1481038125788, 'key_duration': 71, 'keycode': 65}, {'timestamp': 1481038125890, 'key_duration': 173, 'keycode': 16}, {'timestamp': 1481038126178, 'key_duration': 103, 'keycode': 70}, {'timestamp': 1481038126438, 'key_duration': 31, 'keycode': 84}, {'timestamp': 1481038126620, 'key_duration': 54, 'keycode': 69}, {'timestamp': 1481038126732, 'key_duration': 166, 'keycode': 82}, {'timestamp': 1481038126896, 'key_duration': 130, 'keycode': 32}, {'timestamp': 1481038127038, 'key_duration': 2, 'keycode': 65}, {'timestamp': 1481038127126, 'key_duration': 90, 'keycode': 32}, {'timestamp': 1481038127210, 'key_duration': 174, 'keycode': 87}, {'timestamp': 1481038127443, 'key_duration': 2, 'keycode': 72}, {'timestamp': 1481038127559, 'key_duration': 38, 'keycode': 73}, {'timestamp': 1481038127630, 'key_duration': 109, 'keycode': 76}, {'timestamp': 1481038127874, 'key_duration': 79, 'keycode': 69}, {'timestamp': 1481038128025, 'key_duration': 110, 'keycode': 188}, {'timestamp': 1481038128153, 'key_duration': 95, 'keycode': 32}, {'timestamp': 1481038128420, 'key_duration': 87, 'keycode': 70}, {'timestamp': 1481038128513, 'key_duration': 23, 'keycode': 73}, {'timestamp': 1481038128593, 'key_duration': 103, 'keycode': 78}, {'timestamp': 1481038128709, 'key_duration': 79, 'keycode': 68}, {'timestamp': 1481038128859, 'key_duration': 31, 'keycode': 73}, {'timestamp': 1481038128945, 'key_duration': 117, 'keycode': 78}, {'timestamp': 1481038129080, 'key_duration': 1, 'keycode': 71}, {'timestamp': 1481038129192, 'key_duration': 113, 'keycode': 32}, {'timestamp': 1481038129341, 'key_duration': 2, 'keycode': 84}, {'timestamp': 1481038129433, 'key_duration': 33, 'keycode': 72}, {'timestamp': 1481038129528, 'key_duration': 1, 'keycode': 65}, {'timestamp': 1481038129629, 'key_duration': 102, 'keycode': 84}, {'timestamp': 1481038129762, 'key_duration': 116, 'keycode': 32}, {'timestamp': 1481038129880, 'key_duration': 46, 'keycode': 78}, {'timestamp': 1481038129944, 'key_duration': 110, 'keycode': 79}, {'timestamp': 1481038130059, 'key_duration': 22, 'keycode': 84}, {'timestamp': 1481038130140, 'key_duration': 1, 'keycode': 72}, {'timestamp': 1481038130218, 'key_duration': 79, 'keycode': 73}, {'timestamp': 1481038130374, 'key_duration': 118, 'keycode': 78}, {'timestamp': 1481038130491, 'key_duration': 60, 'keycode': 71}, {'timestamp': 1481038130564, 'key_duration': 133, 'keycode': 32}, {'timestamp': 1481038130671, 'key_duration': 29, 'keycode': 77}, {'timestamp': 1481038130766, 'key_duration': 16, 'keycode': 79}, {'timestamp': 1481038130903, 'key_duration': 2, 'keycode': 82}, {'timestamp': 1481038130960, 'key_duration': 59, 'keycode': 69}, {'timestamp': 1481038131026, 'key_duration': 125, 'keycode': 32}, {'timestamp': 1481038131144, 'key_duration': 88, 'keycode': 80}, {'timestamp': 1481038131393, 'key_duration': 66, 'keycode': 8}, {'timestamp': 1481038131591, 'key_duration': 92, 'keycode': 72}, {'timestamp': 1481038131689, 'key_duration': 4, 'keycode': 65}, {'timestamp': 1481038131766, 'key_duration': 81, 'keycode': 80}, {'timestamp': 1481038131970, 'key_duration': 124, 'keycode': 80}, {'timestamp': 1481038132032, 'key_duration': 61, 'keycode': 69}, {'timestamp': 1481038132261, 'key_duration': 109, 'keycode': 78}, {'timestamp': 1481038132405, 'key_duration': 2, 'keycode': 69}, {'timestamp': 1481038132522, 'key_duration': 119, 'keycode': 68}, {'timestamp': 1481038132720, 'key_duration': 1, 'keycode': 188}, {'timestamp': 1481038132832, 'key_duration': 113, 'keycode': 32}, {'timestamp': 1481038132998, 'key_duration': 3, 'keycode': 83}, {'timestamp': 1481038133058, 'key_duration': 63, 'keycode': 72}, {'timestamp': 1481038133206, 'key_duration': 27, 'keycode': 69}, {'timestamp': 1481038133332, 'key_duration': 153, 'keycode': 32}, {'timestamp': 1481038133442, 'key_duration': 39, 'keycode': 68}, {'timestamp': 1481038133505, 'key_duration': 102, 'keycode': 69}, {'timestamp': 1481038133686, 'key_duration': 86, 'keycode': 67}, {'timestamp': 1481038133806, 'key_duration': 103, 'keycode': 73}, {'timestamp': 1481038133970, 'key_duration': 135, 'keycode': 68}, {'timestamp': 1481038134080, 'key_duration': 39, 'keycode': 69}, {'timestamp': 1481038134511, 'key_duration': 1, 'keycode': 68}, {'timestamp': 1481038134622, 'key_duration': 112, 'keycode': 32}, {'timestamp': 1481038134730, 'key_duration': 55, 'keycode': 79}, {'timestamp': 1481038134786, 'key_duration': 2, 'keycode': 78}, {'timestamp': 1481038134865, 'key_duration': 81, 'keycode': 32}, {'timestamp': 1481038135003, 'key_duration': 21, 'keycode': 71}, {'timestamp': 1481038135107, 'key_duration': 41, 'keycode': 79}, {'timestamp': 1481038135159, 'key_duration': 31, 'keycode': 73}, {'timestamp': 1481038135245, 'key_duration': 31, 'keycode': 78}, {'timestamp': 1481038135315, 'key_duration': 17, 'keycode': 71}, {'timestamp': 1481038135388, 'key_duration': 90, 'keycode': 32}, {'timestamp': 1481038135569, 'key_duration': 79, 'keycode': 79}, {'timestamp': 1481038135824, 'key_duration': 55, 'keycode': 8}, {'timestamp': 1481038136042, 'key_duration': 60, 'keycode': 73}, {'timestamp': 1481038136050, 'key_duration': 3, 'keycode': 85}, {'timestamp': 1481038136118, 'key_duration': 23, 'keycode': 78}, {'timestamp': 1481038136157, 'key_duration': 62, 'keycode': 84}, {'timestamp': 1481038136485, 'key_duration': 62, 'keycode': 8}, {'timestamp': 1481038136619, 'key_duration': 47, 'keycode': 8}, {'timestamp': 1481038136968, 'key_duration': 87, 'keycode': 8}, {'timestamp': 1481038137203, 'key_duration': 85, 'keycode': 78}, {'timestamp': 1481038137274, 'key_duration': 69, 'keycode': 84}, {'timestamp': 1481038137420, 'key_duration': 2, 'keycode': 79}, {'timestamp': 1481038137489, 'key_duration': 71, 'keycode': 32}, {'timestamp': 1481038137716, 'key_duration': 71, 'keycode': 84}, {'timestamp': 1481038137865, 'key_duration': 110, 'keycode': 72}]


	test_instance = Behave(data = request.json)
	test_instance_values = test_instance.normalize_data(minmax_values)

	return str(net.activate(test_instance_values))








if __name__ == "__main__":
	# FILES_PATH = sys.argv[1]

	instance = Behave()

	normalized_test_data = instance.normalize_test_data()
	number_of_tests = instance.number_of_tests
	# print normalized_test_data
	normalized_data = normalized_test_data['data']
	resp = normalized_test_data['responses']
	minmax_values = normalized_test_data['min_max']
	# print type(normalized_test_data['data'])


	ds = SupervisedDataSet(3,1)

	resp = []

	for i in range(number_of_tests):
		if (i<2):
			resp.append((1,))
		else:
			resp.append((0,))

		ds.addSample(normalized_data[i], resp[i])


	net = buildNetwork(3,8,1)


	trainer = BackpropTrainer(net, learningrate = 0.01, momentum = 0.99)

	trainer.trainOnDataset(ds, 1000)

	trainer.testOnData()

	app.run(debug=True)
	