# TODO:
# interaction functions

import ast


class Behave():

	def __init__(self, *args, **kwargs):

		self.PATH = "data/user_typing_info/"

		self.data = []


		if (kwargs.get("path")):

			self.PATH = kwargs.get("path")

			self.data = self.read_from_file(self.PATH)


		if (kwargs.get("file")):

			file_name = str(kwargs.get("file"))

			self.data = self.read_from_file(self.PATH+file_name)



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


	def space_delays(self):

		tm_length = len(self.timestamps)

		space_timestamps = [self.timestamps[i] for i in range(tm_length) if self.keycodes[i] == 32]

		space_delays = [space_timestamps[i+1] - space_timestamps[i-1] for i in range(len(space_timestamps) - 1)]

		return space_delays


	def space_delay_average(self):
		"""
		/ tm = timestamps
		Returns average of Space keypress delays.
		Takes an array of timestamps and an array of keycodes as an argument.
		"""
		space_delays = self.space_delays()

		space_tm_average = sum(space_delays) / len(space_delays)

		return space_tm_average



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
				