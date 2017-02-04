import sys

sys.path.append('../')

from server import models

sys.path.append('../../')
from lib import Behave, Keyboard, Mouse

from pybrain.supervised.trainers import BackpropTrainer
from pybrain.datasets.supervised import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork

users = models.Collect.query.all()[15:15+10]
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

ds = SupervisedDataSet(8, user_count)

for index in range(len(normalized_data['responses'])):

	input = normalized_data['data'][index]

	output = normalized_data['responses'][index]
	# print (input, output)

	# print "i: ", input, "...o: ", output
	ds.addSample(input, output)


net = buildNetwork(8, 25,user_count)

trainer = BackpropTrainer(net, learningrate = 0.01, momentum = 0.99)

print "Training network..."
trainer.trainOnDataset(ds, 1000)

trainer.testOnData()

# CHECKING NETWORK
print "Checking network: "

checking_id = 6;

user = users[checking_id]

print "User: ", user.id

keyboard_test_data = user.dataChunk3

mouse_test_data = user.mouseDataChunk3

keyboard_test_instance = Keyboard(data=keyboard_test_data)

mouse_test_instance = Mouse(data=mouse_test_data)

test_data_to_normalize = dict(keyboard_test_instance.get_keyboard_params().items() + mouse_test_instance.get_mouse_params().items())

print test_data_to_normalize

nd = keyboard_test_instance.normalize_data(min_max, test_data_to_normalize)

#print "Normalized data: ", test_data_to_normalize, " / _ / ", nd

print "Response: "

response = net.activate(nd)

print response

result = None

maxResponse = 0

for i in range(len(response)):
	if response[i] > maxResponse:
		result = i
		maxResponse = response[i]

if maxResponse > 0.5: print "Guessed user is: ", users[result].id
else: print "Guessed < 0.5 user is: ", users[result].id 

if users[result].id == user.id: print "TRUE"
else: print "FALSE"