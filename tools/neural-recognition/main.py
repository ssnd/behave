import sys

sys.path.append('../')

from server import models

sys.path.append('../../')
from lib import Behave, Keyboard, Mouse

from pybrain.supervised.trainers import BackpropTrainer
from pybrain.datasets.supervised import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork


hiddenLayers = int(sys.argv[1])
startRange = 4
checkingRange = 20

testingGroup = [2, 3, 7, 8, 9, 11, 12, 13, 15, 16, 17, 18, 19, 22]

#users = models.Collect.query.all()[startRange:startRange+checkingRange]

users = [models.Collect.query.all()[i] for i in testingGroup]

user_count = len(users)

training_data = []

params_count = 0

for user_index in range(len(users)):

	user = users[user_index]

	keyboard_data_chunks = [ user.dataChunk1, user.dataChunk2, user.dataChunk3]

	mouse_data_chunks = [ user.mouseDataChunk1, user.mouseDataChunk2, user.mouseDataChunk3]

	for i in range(len(keyboard_data_chunks)):

		keyboard_instance = Keyboard(data=keyboard_data_chunks[i])

		mouse_instance = Mouse(data=mouse_data_chunks[i])

		params = dict(keyboard_instance.get_keyboard_params().items() + mouse_instance.get_mouse_params().items())

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

trainer = BackpropTrainer(net, learningrate = 0.001, momentum = 0.99, weightdecay = 0.01)

# Network Training

print "Training network with", hiddenLayers, "Hidden Layers..."
trainer.trainOnDataset(ds, 1000)

trainer.testOnData()



# Network Activation

for checkingID in range(len(users)):

	user = users[checkingID]


	keyboard_test_data = user.dataChunk4
	mouse_test_data = user.mouseDataChunk4

	keyboard_test_instance = Keyboard(data=keyboard_test_data)
	mouse_test_instance = Mouse(data=mouse_test_data)

	test_data_to_normalize = dict(keyboard_test_instance.get_keyboard_params().items() + mouse_test_instance.get_mouse_params().items())

	# print "User: ", checkingID, ": ", test_data_to_normalize

	nd = keyboard_test_instance.normalize_data(test_data_to_normalize, _mean, _stddev)

	
	print "Response: "
	response = net.activate(nd)

	print response

	maxResponse = -1

	result = None

	for i in range(len(response)):
		if response[i] > maxResponse:
			maxResponse = response[i]
			result = i

	print "User: ", checkingID

	if maxResponse > 0.5: print "Guessed user: ", result
	else: print "Guessed user: NONE (", result, ")"

	print "------------------------"
	