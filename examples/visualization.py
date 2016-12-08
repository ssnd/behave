# TODO:
# - visualization for each parameter
# - visual comparison between two users

# keypress deltas
# space delays
# backspace count 
# 


# snippet to import the library without relative routes
import sys, os
sys.path.insert(0, os.path.abspath("../.."))

from behave.lib import Behave
import matplotlib.pyplot as plt
import numpy as np

EXAMPLES_PATH = "../data/user_typing_info/"



class Behave_Visualization:

	def  __init__(self):

		pass


	def read_data_file(self, file_index):

		file = open(EXAMPLES_PATH + str(file_index), "r")

		contents = file.read()

		instance = Behave(data=contents)

		return instance


	def keypress_delay_deltas(self, file_index):

		instance = self.read_data_file(file_index)

		deltas = instance.keypress_delay_deltas()

		plt.plot(deltas)

		plt.show()


	def compare_delay_deltas(self, deg=0, *args):

		all_deltas = []

		avgs = []

		plt.figure()

		for count, file_index in enumerate(args):

			instance = self.read_data_file(file_index)

			deltas = instance.keypress_delay_deltas()

			x = [i for i in range(len(deltas))]

			if (deg==0) :

				avg = sum(deltas)/len(deltas)

				avgs.append(avg)

				avg_dict = [avg for i in range(len(deltas))]

				plt.plot(x, avg_dict, "--r")

			else:

				polyfit = np.polyfit(x,deltas,deg)

				u = np.linspace(1,len(deltas), 20)

				v = np.polyval(polyfit, u)

				plt.plot(u,v, "--r")

			plt.plot(x,deltas, ".")

			all_deltas.append(deltas)

		plt.grid(True)

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

	def compare_space_delays(self, *args):

		all_delays = []

		for count, file_index in enumerate(args):

			instance = self.read_data_file(file_index)

			delay = instance.space_delays()

			plt.plot(delay[1:])

			all_delays.append(delay)

		plt.show()

		return all_delays


	def compare_keypress_durations(self, *args):

		all_delays = []

		for count, file_index in enumerate(args):

			instance = self.read_data_file(file_index)

			delay = instance.keypress_durations()

			plt.plot(delay)

			all_delays.append(delay)
			
			avg = sum(delay)/len(delay)

			avg_dict = [avg for i in range(len(delay))]

			plt.plot(avg_dict)

		plt.show()

		return all_delays



Behave_Visualization().compare_keypress_durations(1, 2)

# print instance.keypress_delay_average()

