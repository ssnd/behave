from lib.behave import Behave
import pybrain
from pybrain.datasets import *
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer


path = "data/user_typing_info/"

number_of_tests = 4

params_arr = []

for i in range(1,number_of_tests+1):
	instance = Behave(path=path+str(i))
	params_arr.append(instance.get_all_params())


data = []

for instance in params_arr:
	params_arr = [instance[key]*1.0 for key in sorted(instance)]
	data.append(params_arr)

avg_data_arr = [] 

for i in range(len(instance)):
	param_data = zip(*data)[i]
	maxv = max(param_data)
	minv = min(param_data)
	avg_data = [(val-minv)/(maxv-minv) for val in param_data]
	avg_data_arr.append(avg_data)

user_data = []
resp = []

for i in range(number_of_tests):
	if i<2:
		resp.append((0,1))
	else:
		resp.append((1,0))

	user_data.append(zip(*avg_data_arr)[i])


ds = SupervisedDataSet(3,2)

for i in range(4):
	ds.addSample(user_data[i], resp[i])


net = buildNetwork(3,8,2)

trainer = BackpropTrainer(net, learningrate = 0.01, momentum = 0.99)
trainer.trainOnDataset(ds, 1000)
trainer.testOnData()


print net.activate((0.0, 0.6153846153846154, 1.0))
print net.activate((0.3157894736842105, 1.0, 0.6621007063196948))
print net.activate((1.0, 0.6153846153846154, 0.0))
print net.activate((0.7368421052631579, 0.0, 0.20030942539287358))