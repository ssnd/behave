import ast
import os
import math


class Behave():

	def __init__(self, *args, **kwargs):

		self.data = []

		if (kwargs.get("file")):

			file_name = str(kwargs.get("file"))

			self.data = self.read_from_file(self.PATH+file_name)


		if (kwargs.get("data")):

			self.data = kwargs.get("data")


		# if the passed in data is text, convert it to json
		if (type(self.data) == str):

			self.data = ast.literal_eval(self.data)


	def read_from_file(self, path):

		f = open(path, "r")

		file_contents = f.read()

		return file_contents


	@staticmethod
	def average(arr):
		"""calculate average from a given array of data
		
		Args:
			arr (Array): Input array
		
		Returns:
			Array: Calculated average
		"""
		return sum(arr) / len(arr)

	@staticmethod
	def standart_deviation(arr):
		"""Calculate the standart deviation of the array
		
		Args:
			arr (Array): Input array
		
		Returns:
			Number: Calculated deviation
		"""
		length = len(arr)

		average = sum(arr) / length

		deviations = [(i-average)**2 for i in arr]

		variance = sum(deviations)/length

		deviation = math.sqrt(variance)

		return deviation

	def normalize_data(self, params, mean, stddev):

		normalized_data = []

		for param in params:

			val = params[param]

			calc_val = (val - mean[param]) / stddev[param]

			normalized_data.append(calc_val)

		return tuple(normalized_data)



	@staticmethod
	def normalize_training_data(training_data):
		"""Normalizes the passed training data and prepares it for use in neural network. (Gaussian Normalization)
		
		Args:
			training_data (array): The array should consist of dictionaries. Each should have two indexes: 
				1) 'data' - the data generated by the get_all_params() method
				2) 'response' - index of the neuron which must be set to 1.

		Returns:
			dict: Returns a dictionary with the following indexes:
				1) 'data' : tuples with input data for training
				2) 'responses' : tuples with responses for training
				3) 'mean' : mean values of gaussian normalization
				4) 'stddev' : standart deviation values of gaussian normalization
		"""
		resp = []
		resp_ids = []
		data=[]
		avg_data_arr=[]

		params_dict = {}

		param_mean = {}
		param_stddev = {}

		for key in training_data[0]['data']: params_dict[key] = []

		for i in range(len(training_data)):

			user_params = training_data[i]['data']

			for param in user_params:
				params_dict[param].append(user_params[param] * 1.0)

			resp_ids.append(training_data[i]['response'])

		# calculating mean and stddev for every parameter

		for param in params_dict:
			
			param_data = params_dict[param]

			param_mean[param] = Behave.average(param_data)

			param_stddev[param] = Behave.standart_deviation(param_data)

		
		for param in params_dict:
			
			param_data = params_dict[param]

			avg_data = [((val - param_mean[param])/param_stddev[param])*1.0 for val in param_data]

			avg_data_arr.append(avg_data)


		data = [zip(*avg_data_arr)[i] for i in range(len(training_data))]
		
		maxlen = max(resp_ids)+1

		for i in range(len(resp_ids)):
			new_arr = []
			for j in range(maxlen):

				if j==resp_ids[i]:
					new_arr.append(1)
					continue

				new_arr.append(0)

			arr_tuple = tuple(new_arr)
			resp.append(arr_tuple)

		user_data = {
			"data" : data,
			"responses" : resp,
			"mean" : param_mean,
			"stddev": param_stddev
		}

		return user_data