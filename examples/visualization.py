# TODO:
# - visualization for each parameter
# - visual comparison between two users


# snippet to import the library without relative routes
import sys, os
sys.path.insert(0, os.path.abspath("../.."))

from behave.lib import Behave
import matplotlib.pyplot as plt

EXAMPLES_PATH = "../data/user_typing_info/"



class Behave_Visualization:

	def  __init__(self):

		pass


	def read_data_file(self, file_index):

		file = open(EXAMPLES_PATH + str(file_index), "r")

		contents = file.read()

		instance = Behave(contents)

		return instance


	def keypress_delay_deltas(self, file_index):

		instance = self.read_data_file(file_index)

		deltas = instance.keypress_delay_deltas()

		plt.plot(deltas)

		plt.show()


	def compare_delay_deltas(self, *args):

		all_deltas = []

		for count, file_index in enumerate(args):

			instance = self.read_data_file(file_index)

			deltas = instance.keypress_delay_deltas()

			plt.plot(deltas)

			all_deltas.append(deltas)

		plt.show()
		
		return all_deltas

	def compare_keypress_delays(self, *args):

		all_delays = []

		for count, file_index in enumerate(args):

			instance = self.read_data_file(file_index)

			delay = instance.keypress_delay_average()

			plt.hist(int(delay),[0,1])

			all_delays.append(delay)



		# plt.axis([0, count, 0, int(max(all_delays))])				

		plt.show()

		return all_delays






print Behave_Visualization().compare_delay_deltas(1,2)

# print instance.keypress_delay_average()










