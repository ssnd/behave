from behave import Behave
import ast, os, math
from scipy.spatial import distance

class Mouse(Behave):
	"""
	Instance of the Behave class. Gathers the mouse dynamics information.


	"""
	def __init__(self, data):


		self.right_click_durations			= []
		
		self.left_click_durations			= []

		self.left_click_timestamps			= []

		self.dbclick_durations				= []

		self.mouse_move_events				= []

		self.point_and_click_durations		= []

		self.move_distances 				= []


		Behave.__init__(self, data)

		self.data = data

		if (type(data) == str) :
			self.data = ast.literal_eval(data)
		



		# filter mouse events
		for index,chunk in enumerate(self.data):
			# find and filter mouse moves
			if chunk['event'] == "mousemove":
				self.mouse_move_events.append(chunk)

			# find and filter the clicks and durations
			if chunk['event'] == "leftClick" or chunk['event'] == "rightClick":
				
				if (self.data[index-1]['event']=="mousemove"):

					point_and_click_duration = int(chunk['mousePress']) - int(self.data[index-1]['timestamp'])
					self.point_and_click_durations.append(point_and_click_duration)


				press_timestamp = int(chunk['mousePress'])
				release_timestamp = int(chunk['mouseRelease'])

				duration = release_timestamp - press_timestamp

				if chunk['event'] == "leftClick":
					self.left_click_durations.append(duration)
					self.left_click_timestamps.append(chunk['mousePress'])

				if chunk['event'] == "rightClick":
					self.right_click_durations.append(duration)



		# search for mouse move distance average
		pause_index = [0]

		for i,c in enumerate(self.mouse_move_events):

			if i > 0:

				diff = int(c['timestamp']) - int(self.mouse_move_events[i-1]['timestamp'])


				if (diff>300 or i==len(self.mouse_move_events)-1):

					pause_index.append(i)

					length = len(pause_index)

					begin_x = int(self.mouse_move_events[pause_index[length-2]]["mouseX"])
					begin_y = int(self.mouse_move_events[pause_index[length-2]]["mouseY"])


					end_x = int(self.mouse_move_events[i]["mouseX"])
					end_y = int(self.mouse_move_events[i]['mouseY'])

					begin_coords = (begin_x, begin_y)
					end_coords = (end_x, end_y)

					self.move_distances.append(distance.euclidean(begin_coords,end_coords))



		# search for doubleclicks
		for i in range(1, len(self.left_click_timestamps)):
			diff = int(self.left_click_timestamps[i]) - int(self.left_click_timestamps[i-1])
			if (diff<350):
				self.dbclick_durations.append(diff)

		self.mousemove_timestamps = [chunk['timestamp'] for chunk in self.mouse_move_events]







	def get_mouse_params(self):
		"""
		Returns an array of all analyzed values as a dictionary
		"""
		val_arr = {}

		val_arr['left_click_duration_avg'] = self.average(self.left_click_durations)

		val_arr['right_click_duration_avg'] = self.average(self.right_click_durations)

		val_arr['double_click_duration_avg'] = self.average(self.dbclick_durations)

		#val_arr['point_and_click_duration_avg'] = self.average(self.point_and_click_durations)

		#val_arr['move_distance_avg'] = self.average(self.move_distances)

		val_arr['left_click_duration_deviation'] = self.standart_deviation(self.left_click_durations)

		val_arr['right_click_duration_deviation'] = self.standart_deviation(self.right_click_durations)

		val_arr['double_click_duration_deviation'] = self.standart_deviation(self.dbclick_durations)

		val_arr['point_and_click_duration_deviation'] = self.standart_deviation(self.point_and_click_durations)

		#val_arr['move_distance_deviation'] = self.standart_deviation(self.move_distances)


		return val_arr

	
