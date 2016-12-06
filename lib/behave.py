# TODO:
# kps analysis
# interaction functions

import json

class Behave_Utils():

	def __init__(self):
		pass

	def read_from_file(self, path):

		f = open(path, "r")
		
		file_contents = f.read()

		return file_contents


class Behave():

	def __init__(self, data):


		# if the data passed in is text, convert it to json
		if (type(data) == str):

			data = json.loads(data)

		self.timestamps = [keypress['timestamp'] for keypress in data]

		self.durations = [keypress['key_duration'] for keypress in data]

		self.keycodes = [keypress['keycode'] for keypress in data]


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

		tm_all_time_s = tm_all_time_ms / 100

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


	def backspace_count(self):
		"""
		Returns Backspace keypress count.
		Takes array of keycodes as an argument.
		"""
		return self.keycodes.count(8)


	def keypress_duration_average(self):
		"""
		/ key_d = key_duration
		Returns average of keypress durations.
		Takes array of keypress durations as an argument.
		"""
		return sum(self.durations) / len(self.durations)


	def space_delay_average(self):
		"""
		/ tm = timestamps
		Returns average of Space keypress delays.
		Takes an array of timestamps and an array of keycodes as an argument.
		"""
		tm_length = len(self.timestamps)

		space_timestamps = [self.timestamps[i] for i in range(tm_length) if self.keycodes[i] == 32]

		space_delays = [space_timestamps[i+1] - space_timestamps[i-1] for i in range(len(space_timestamps) - 1)]

		space_tm_average = sum(space_delays) / len(space_delays)

		return space_tm_average




if __name__ == "__main__":


	data = [{u'timestamp': 1480518416394, u'key_duration': 44, u'keycode': 83}, 
	{u'timestamp': 1480518416452, u'key_duration': 53, u'keycode': 65}, 
	{u'timestamp': 1480518416499, u'key_duration': 100, u'keycode': 78}, 
	{u'timestamp': 1480518416870, u'key_duration': 36, u'keycode': 16}, 
	{u'timestamp': 1480518416893, u'key_duration': 59, u'keycode': 36}, 
	{u'timestamp': 1480518416956, u'key_duration': 122, u'keycode': 8}, 
	{u'timestamp': 1480518417283, u'key_duration': 125, u'keycode': 17}, 
	{u'timestamp': 1480518417778, u'key_duration': 94, u'keycode': 17}, 
	{u'timestamp': 1480518417825, u'key_duration': 141, u'keycode': 17}, 
	{u'timestamp': 1480518417825, u'key_duration': 141, u'keycode': 16}, 
	{u'timestamp': 1480518417969, u'key_duration': 98, u'keycode': 76}, 
	{u'timestamp': 1480518418166, u'key_duration': 112, u'keycode': 79}, 
	{u'timestamp': 1480518418301, u'key_duration': 53, u'keycode': 82}, 
	{u'timestamp': 1480518418379, u'key_duration': 131, u'keycode': 69}, 
	{u'timestamp': 1480518418545, u'key_duration': 97, u'keycode': 77}, 
	{u'timestamp': 1480518418571, u'key_duration': 123, u'keycode': 32}, 
	{u'timestamp': 1480518418734, u'key_duration': 50, u'keycode': 73}, 
	{u'timestamp': 1480518418783, u'key_duration': 99, u'keycode': 77}, 
	{u'timestamp': 1480518419084, u'key_duration': 82, u'keycode': 8}, 
	{u'timestamp': 1480518419399, u'key_duration': 99, u'keycode': 80}, 
	{u'timestamp': 1480518419575, u'key_duration': 41, u'keycode': 83}, 
	{u'timestamp': 1480518419617, u'key_duration': 83, u'keycode': 85}, 
	{u'timestamp': 1480518419916, u'key_duration': 112, u'keycode': 32}, 
	{u'timestamp': 1480518420151, u'key_duration': 78, u'keycode': 8}, 
	{u'timestamp': 1480518420367, u'key_duration': 35, u'keycode': 77},
	{u'timestamp': 1480518420400, u'key_duration': 0, u'keycode': 32}, 
	{u'timestamp': 1480518420514, u'key_duration': 16, u'keycode': 68}, 
	{u'timestamp': 1480518420583, u'key_duration': 85, u'keycode': 79}, 
	{u'timestamp': 1480518420798, u'key_duration': 121, u'keycode': 76}, 
	{u'timestamp': 1480518420983, u'key_duration': 107, u'keycode': 79}, 
	{u'timestamp': 1480518421116, u'key_duration': 117, u'keycode': 32}, 
	{u'timestamp': 1480518421335, u'key_duration': 0, u'keycode': 8}, 
	{u'timestamp': 1480518421444, u'key_duration': 59, u'keycode': 82}, 
	{u'timestamp': 1480518422487, u'key_duration': 53, u'keycode': 69}, 
	{u'timestamp': 1480518422533, u'key_duration': 99, u'keycode': 84}, 
	{u'timestamp': 1480518422828, u'key_duration': 61, u'keycode': 16}, 
	{u'timestamp': 1480518422851, u'key_duration': 84, u'keycode': 49}]

	behave = Behave(data)

	print(behave.keypress_delay_deltas())
	print(len(data))
	print(keypress_delay_average(timestamps))
	print(backspace_count(keycodes))
	print(keypress_duration_average(durations))
	print(space_delay_average(timestamps, keycodes))
