import sys

sys.path.append('../../')
from lib import Behave, Keyboard, Mouse

import rethinkdb as r

import operator

from pybrain.supervised.trainers import BackpropTrainer
from pybrain.datasets.supervised import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork

r.connect("localhost", 28015).repl()

user_id_list = r.table("users").run()
user_list = []

for user_id in user_id_list:
	user_id = user_id["id"]

	user = {}

	user["user_keypresses"] = []

	for key_group in r.table("keypresses").filter(r.row["user_id"]==user_id).get_field("keypressGroup_id").distinct().run():
		key_group_chunk = [k for k in r.table("keypresses").filter(r.row["keypressGroup_id"] == key_group).run()]
		key_group_chunk.sort(key=operator.itemgetter("keyPress"))
		if len(key_group_chunk) > 2:
			user["user_keypresses"].append(key_group_chunk)
		
	user_list.append(user)


#hiddenLayers = int(sys.argv[1])
hiddenLayers = 27

_lrate = 0.0055
_lrdecay = 1.0
_momentum = 0
_weightdecay = 0


training_data = []

params_count = 0

user_count = len(user_list)


for user_index in range(len(user_list)):

	user = user_list[user_index]

	keyboard_data_chunks = []

	#mouse_data_chunks = []

	for key_group in user["user_keypresses"]:
		keyboard_data_chunks.append(key_group)


	for i in range(len(keyboard_data_chunks)):

		keyboard_instance = Keyboard(data=keyboard_data_chunks[i])

		#mouse_instance = Mouse(data=mouse_data_chunks[i])

		params = dict(keyboard_instance.get_keyboard_params().items()) # + mouse_instance.get_mouse_params().items())

		params_count = len(params)

		prepared_dict = {
			"data" : params,
			"response" : user_index
		}


		training_data.append(prepared_dict)

normalized_data = Behave.normalize_training_data(training_data)

_mean, _stddev = normalized_data["mean"], normalized_data["stddev"]

# Setting Dataset For Network

ds = SupervisedDataSet(params_count, user_count)

for index in range(len(normalized_data['responses'])):

	input = normalized_data['data'][index]

	output = normalized_data['responses'][index]

	ds.addSample(input, output)

# Network Initialization

net = buildNetwork(params_count, hiddenLayers, user_count)


trainer = BackpropTrainer(net, learningrate = _lrate, momentum = _momentum, weightdecay = _weightdecay, lrdecay = _lrdecay)

# Network Training

print "Training network with", hiddenLayers, "Hidden Layers..."
trainer.trainOnDataset(ds, 1000)

trainer.testOnData()

keyboard_test_data = user_list[0]["user_keypresses"][0]

keyboard_test_instance = Keyboard(data=keyboard_test_data)
#mouse_test_instance = Mouse(data=mouse_test_data)

test_data_to_normalize = dict(keyboard_test_instance.get_keyboard_params().items()) # + mouse_test_instance.get_mouse_params().items())

# print "User: ", checkingID, ": ", test_data_to_normalize

nd = keyboard_test_instance.normalize_data(test_data_to_normalize, _mean, _stddev)
response = net.activate(nd)
print response