# TODO:
# interaction functions

import ast
import os


class Behave():

	def __init__(self, *args, **kwargs):

		self.PATH = "../data/user_typing_info/"

		if (kwargs.get("path")):

			self.PATH = kwargs.get("path")




		self.data = []


		path, dirs, files = os.walk(self.PATH).next()

		if (kwargs.get("file")):

			file_name = str(kwargs.get("file"))

			self.data = self.read_from_file(self.PATH+file_name)

		self.number_of_tests = len(files)


		if (kwargs.get("data")):

			self.data = kwargs.get("data")


		# if the data passed in is text, convert it to json
		if (type(self.data) == str):

			self.data = ast.literal_eval(self.data)


		self.timestamps = [keypress['timestamp'] for keypress in self.data]

		self.durations = [keypress['key_duration'] for keypress in self.data]

		self.keycodes = [keypress['keycode'] for keypress in self.data]



	def read_from_file(self, path):

		f = open(path, "r")
		
		file_contents = f.read()

		return file_contents



	def keypress_delay_deltas(self):

		delays = [self.timestamps[i+1] - self.timestamps[i] for i in range(len(self.timestamps) - 1)]

		return delays


	def keypress_per_second(self):
		"""
		/ tm = timestamps
		Returns decimal count of keypress per second (KPS).
		Takes an array of timestamps as an argument.
		"""
		tm_all_time_ms = self.timestamps[-1] - self.timestamps[0]

		tm_all_time_s = tm_all_time_ms / 100.0

		tm_key_count = len(self.timestamps)

		tm_key_per_sec = tm_key_count / tm_all_time_s
		
		return tm_key_per_sec

	
	def keypress_delay_average(self):
		"""
		/ tm = timestamps
		Returns average of delays between timestamps.
		Takes array of timestamps as an argument.
		"""
		tm_length = len(self.timestamps)

		delays = self.keypress_delay_deltas()

		tm_average = sum(delays) / tm_length

		return tm_average


	def keypress_durations(self):
		
		return self.durations


	def keypress_duration_average(self):
		"""
		/ key_d = key_duration
		Returns average of keypress durations.
		Takes array of keypress durations as an argument.
		"""
		return sum(self.durations) / len(self.durations)


	def average_difference(self, subject):
		"""
		/ subject = other test with comparision data.
		Returns differences between subject and object tests.
		"""
		kps_diff = abs(self.keypress_per_second() - subject.keypress_per_second())

		kdel_diff = abs(self.keypress_delay_average() - subject.keypress_delay_average())

		kdur_diff = abs(self.keypress_duration_average() - subject.keypress_duration_average())

		return {"kps_diff": kps_diff, "kdel_diff": kdel_diff, "kdur_diff": kdur_diff}


	def get_all_params(self):
		"""
		Returns an array of all analyzed values as a dictionary
		"""

		val_arr = {}

		val_arr['kps'] = self.keypress_per_second()

		val_arr['kdel'] = self.keypress_delay_average()

		val_arr['kdur'] = self.keypress_duration_average()


		return val_arr



	def compare_difference(self, subject):
		"""
		/ subject = other test with comparision data.
		Returns True for the same user and False for different users.
		"""

		# maximum differences for the same user

		max_kps_diff = 0.06

		max_kdel_diff = 10

		max_kdur_diff = 10
	

		difference = self.average_difference(subject)

		kps_diff = difference["kps_diff"]

		kdel_diff = difference["kdel_diff"]

		kdur_diff = difference["kdur_diff"]

		
		return kps_diff < max_kps_diff and kdel_diff < max_kdel_diff and kdur_diff < max_kdur_diff


	def normalize_data(self, min_max_values):

		user_data = self.get_all_params()

		user_data_values = user_data.values()

		normalized_data = []

		for key in range(len(user_data_values)):

			minv = min_max_values[key][0]
			maxv = min_max_values[key][1]

			value = user_data_values[key]

			calc_val = (value-minv)/(maxv-minv)

			normalized_data.append(calc_val)

		return tuple(normalized_data)

	def normalize_test_data(self):

		"""
		normalize data and prepare it for use in neural network
		"""

		params_arr = []

		for i in range(1, self.number_of_tests+1):

			instance = Behave(file=i, path=self.PATH)

			params_dict = instance.get_all_params()

			params_arr.append([params_dict[key]*1.0 for key in params_dict])


		min_max_values = []
		avg_data_arr = []


		for i in range(len(params_dict)):
			param_data = zip(*params_arr)[i]

			maxv = max(param_data)
			minv = min(param_data)

			min_max = (minv, maxv)

			min_max_values.append(min_max)

			avg_data = [(val-minv)/(maxv-minv) for val in param_data]

			avg_data_arr.append(avg_data)


		data = [zip(*avg_data_arr)[i] for i in range(self.number_of_tests)]

		resp = []

		# todo: fix this shit
		for i in range(self.number_of_tests):
			if i < 2:
				resp.append((1,))
			else:
				resp.append((0,))

		user_data = {
			"data" : data,
			"responses" : resp,
			"min_max" : min_max_values
		}

		return user_data



if __name__ == "__main__":

	behave_instance = Behave()

	data = behave_instance.normalize_test_data()
	print type(data)


