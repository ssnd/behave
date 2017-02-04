import sys

sys.path.append('../')

from server import models

sys.path.append('../../')
from lib import Behave, Keyboard, Mouse

from pybrain.supervised.trainers import BackpropTrainer
from pybrain.datasets.supervised import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork


hiddenLayers = 6
startRange = 5
checkingRange = 3


users = models.Collect.query.all()[startRange:startRange+checkingRange]

user_count = len(users)

training_data = []

for user_index in range(len(users)):

	user = users[user_index]

	keyboard_data_chunks = [user.dataChunk1, user.dataChunk2, user.dataChunk3]

	mouse_data_chunks = [user.mouseDataChunk1, user.mouseDataChunk2, user.mouseDataChunk3]

	for i in range(len(keyboard_data_chunks)):

		keyboard_instance = Keyboard(data=keyboard_data_chunks[i])

		mouse_instance = Mouse(data=mouse_data_chunks[i])

		params = dict(keyboard_instance.get_keyboard_params().items() + mouse_instance.get_mouse_params().items())

		prepared_dict = {
			"data" : params,
			"response" : user_index
		}


		training_data.append(prepared_dict)

normalized_data = Behave.normalize_training_data(training_data)


min_max = normalized_data['min_max']

# Setting Dataset For Network

ds = SupervisedDataSet(8, user_count)

for index in range(len(normalized_data['responses'])):

	input = normalized_data['data'][index]

	output = normalized_data['responses'][index]

	ds.addSample(input, output)


# Network Initialization

net = buildNetwork(8, hiddenLayers, user_count)

trainer = BackpropTrainer(net, learningrate = 0.01, momentum = 0.99)

# Network Training

print "Training network with", hiddenLayers, "Hidden Layers..."
trainer.trainOnDataset(ds, 1000)

trainer.testOnData()

# Network Activation

for checkingID in range(checkingRange):

	user = users[checkingID]


	keyboard_test_data = user.dataChunk4
	mouse_test_data = user.mouseDataChunk4

	keyboard_test_instance = Keyboard(data=keyboard_test_data)
	mouse_test_instance = Mouse(data=mouse_test_data)

	test_data_to_normalize = dict(keyboard_test_instance.get_keyboard_params().items() + mouse_test_instance.get_mouse_params().items())

	nd = keyboard_test_instance.normalize_data(min_max, test_data_to_normalize)

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
	else: print "Guessed user: NONE"

	print "------------------------"