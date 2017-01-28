import sys

sys.path.append('../')

from server import models

sys.path.append('../../')
from lib import Behave, Keyboard, Mouse

from pybrain.supervised.trainers import BackpropTrainer
from pybrain.datasets.supervised import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork

users = models.Collect.query.all()
user_count = len(users)

training_data = []

for user_index in range(len(users)):

	user = users[user_index]

	keyboard_data_chunks = [user.dataChunk1, user.dataChunk2, user.dataChunk3]

	mouse_data_chunks = [user.mouseDataChunk1, user.mouseDataChunk2, user.mouseDataChunk3]

	for data_chunk in keyboard_data_chunks:

		instance = Keyboard(data=data_chunk)

		params = instance.get_keyboard_params()

		prepared_dict = {
			"data" : params,
			"response" : user_index
		}


		training_data.append(prepared_dict)

	for mouse_data_chunk in mouse_data_chunks:

		instance = Mouse(data=mouse_data_chunk)

		params = instance.get_mouse_params()

		prepared_dict = {
			"data" : params, 
			"response" : user_index
		}

		training_data.append(prepared_dict)

normalized_data = Behave.normalize_training_data(training_data)


min_max = normalized_data['min_max']

ds = SupervisedDataSet(4, user_count)

for index in range(len(normalized_data['responses'])):

	input = normalized_data['data'][index]

	output = normalized_data['responses'][index]
	# print (input, output)
	ds.addSample(input, output)


net = buildNetwork(4,(3+user_count)*2,user_count)

trainer = BackpropTrainer(net, learningrate = 0.01, momentum = 0.99)

print "Training network..."
trainer.trainOnDataset(ds, 1000)

trainer.testOnData()

print min_max


# CHECKING NETWORK
print "Checking network: "
user = users[7]

print "User: ", user.id

data = user.dataChunk4

instance = Keyboard(data=data)

print instance.get_keyboard_params()

nd = instance.normalize_data(min_max, instance.get_keyboard_params())
print nd

print "Response: "

response = net.activate(nd)

print response

result = None

for i in range(len(response)):
	if response[i] > 0.5: result = i

print result

guessed_user = users[result]

print "Guessed user is: ", guessed_user.id
