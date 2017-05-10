from behave import Behave
import ast, os, math
from scipy.spatial import distance

class Mouse(Behave):
	"""Instance of the Behave class. Gathers the mouse dynamics information.


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

		val_arr['point_and_click_duration_avg'] = self.average(self.point_and_click_durations)

		val_arr['move_distance_avg'] = self.average(self.move_distances)

		val_arr['left_click_duration_deviation'] = self.standart_deviation(self.left_click_durations)

		val_arr['right_click_duration_deviation'] = self.standart_deviation(self.right_click_durations)

		val_arr['double_click_duration_deviation'] = self.standart_deviation(self.dbclick_durations)

		val_arr['point_and_click_duration_deviation'] = self.standart_deviation(self.point_and_click_durations)

		val_arr['move_distance_deviation'] = self.standart_deviation(self.move_distances)


		return val_arr



if __name__ == "__main__":
	data ={"data":[{"mouseX":325,"mouseY":30,"timestamp":1484041775012,"event":"mousemove"},{"mouseX":325,"mouseY":30,"timestamp":1484041775106,"event":"mousemove"},{"mouseX":225,"mouseY":88,"timestamp":1484041775417,"event":"mousemove"},{"mouseX":86,"mouseY":142,"timestamp":1484041775606,"event":"mousemove"},{"mouseX":0,"mouseY":134,"timestamp":1484041775706,"event":"mousemove"},{"mouseX":0,"mouseY":134,"timestamp":1484041775856,"event":"leftClick","duration":19},{"mouseX":15,"mouseY":131,"timestamp":1484041776006,"event":"mousemove"},{"mouseX":127,"mouseY":153,"timestamp":1484041776106,"event":"mousemove"},{"mouseX":124,"mouseY":156,"timestamp":1484041776206,"event":"mousemove"},{"mouseX":124,"mouseY":156,"timestamp":1484041776218,"event":"leftClick","duration":19},{"mouseX":118,"mouseY":151,"timestamp":1484041776406,"event":"mousemove"},{"mouseX":62,"mouseY":117,"timestamp":1484041776506,"event":"mousemove"},{"mouseX":62,"mouseY":117,"timestamp":1484041776635,"event":"leftClick","duration":25},{"mouseX":415,"mouseY":293,"timestamp":1484041776906,"event":"mousemove"},{"mouseX":440,"mouseY":312,"timestamp":1484041777006,"event":"mousemove"},{"mouseX":482,"mouseY":345,"timestamp":1484041777106,"event":"mousemove"},{"mouseX":544,"mouseY":417,"timestamp":1484041777206,"event":"mousemove"},{"mouseX":636,"mouseY":514,"timestamp":1484041777306,"event":"mousemove"},{"mouseX":632,"mouseY":489,"timestamp":1484041777406,"event":"mousemove"},{"mouseX":606,"mouseY":450,"timestamp":1484041777506,"event":"mousemove"},{"mouseX":589,"mouseY":443,"timestamp":1484041777606,"event":"mousemove"},{"mouseX":589,"mouseY":443,"timestamp":1484041777699,"event":"leftClick","duration":33},{"mouseX":537,"mouseY":354,"timestamp":1484041777906,"event":"mousemove"},{"mouseX":487,"mouseY":56,"timestamp":1484041778005,"event":"mousemove"},{"mouseX":563,"mouseY":48,"timestamp":1484041778106,"event":"mousemove"},{"mouseX":607,"mouseY":108,"timestamp":1484041778206,"event":"mousemove"},{"mouseX":603,"mouseY":127,"timestamp":1484041778352,"event":"mousemove"},{"mouseX":603,"mouseY":127,"timestamp":1484041779028,"event":"rightClick","duration":24},{"mouseX":599,"mouseY":130,"timestamp":1484041779306,"event":"mousemove"},{"mouseX":291,"mouseY":370,"timestamp":1484041779405,"event":"mousemove"},{"mouseX":96,"mouseY":453,"timestamp":1484041779506,"event":"mousemove"},{"mouseX":93,"mouseY":456,"timestamp":1484041779606,"event":"mousemove"},{"mouseX":68,"mouseY":458,"timestamp":1484041779806,"event":"mousemove"},{"mouseX":68,"mouseY":458,"timestamp":1484041779856,"event":"leftClick","duration":27},{"mouseX":266,"mouseY":314,"timestamp":1484041780107,"event":"mousemove"},{"mouseX":449,"mouseY":66,"timestamp":1484041780205,"event":"mousemove"},{"mouseX":410,"mouseY":90,"timestamp":1484041780311,"event":"mousemove"},{"mouseX":282,"mouseY":211,"timestamp":1484041780406,"event":"mousemove"},{"mouseX":272,"mouseY":223,"timestamp":1484041780506,"event":"mousemove"},{"mouseX":276,"mouseY":229,"timestamp":1484041780606,"event":"mousemove"},{"mouseX":276,"mouseY":229,"timestamp":1484041781097,"event":"rightClick","duration":30},{"mouseX":335,"mouseY":321,"timestamp":1484041781408,"event":"mousemove"},{"mouseX":394,"mouseY":427,"timestamp":1484041781507,"event":"mousemove"},{"mouseX":387,"mouseY":409,"timestamp":1484041781707,"event":"mousemove"},{"mouseX":375,"mouseY":403,"timestamp":1484041781807,"event":"mousemove"},{"mouseX":375,"mouseY":403,"timestamp":1484041781920,"event":"leftClick","duration":27},{"mouseX":386,"mouseY":293,"timestamp":1484041782208,"event":"mousemove"},{"mouseX":418,"mouseY":215,"timestamp":1484041782353,"event":"mousemove"},{"mouseX":420,"mouseY":217,"timestamp":1484041782407,"event":"mousemove"},{"mouseX":425,"mouseY":223,"timestamp":1484041782507,"event":"mousemove"},{"mouseX":441,"mouseY":196,"timestamp":1484041782607,"event":"mousemove"},{"mouseX":442,"mouseY":190,"timestamp":1484041782707,"event":"mousemove"},{"mouseX":442,"mouseY":190,"timestamp":1484041782952,"event":"rightClick","duration":23},{"mouseX":355,"mouseY":209,"timestamp":1484041783407,"event":"mousemove"},{"mouseX":299,"mouseY":228,"timestamp":1484041783506,"event":"mousemove"},{"mouseX":314,"mouseY":222,"timestamp":1484041783607,"event":"mousemove"},{"mouseX":313,"mouseY":227,"timestamp":1484041783707,"event":"mousemove"},{"mouseX":313,"mouseY":227,"timestamp":1484041783833,"event":"leftClick","duration":17},{"mouseX":313,"mouseY":227,"timestamp":1484041783954,"event":"leftClick","duration":19},{"mouseX":313,"mouseY":227,"timestamp":1484041783958,"event":"dbclick","duration":121},{"mouseX":317,"mouseY":237,"timestamp":1484041784207,"event":"mousemove"},{"mouseX":355,"mouseY":357,"timestamp":1484041784309,"event":"mousemove"},{"mouseX":354,"mouseY":388,"timestamp":1484041784407,"event":"mousemove"},{"mouseX":354,"mouseY":384,"timestamp":1484041784697,"event":"leftClick","duration":18},{"mouseX":354,"mouseY":384,"timestamp":1484041784842,"event":"leftClick","duration":23},{"mouseX":354,"mouseY":384,"timestamp":1484041784851,"event":"dbclick","duration":145},{"mouseX":410,"mouseY":255,"timestamp":1484041785107,"event":"mousemove"},{"mouseX":460,"mouseY":161,"timestamp":1484041785207,"event":"mousemove"},{"mouseX":463,"mouseY":161,"timestamp":1484041785512,"event":"leftClick","duration":16},{"mouseX":463,"mouseY":161,"timestamp":1484041785643,"event":"leftClick","duration":19},{"mouseX":463,"mouseY":161,"timestamp":1484041785648,"event":"dbclick","duration":131},{"mouseX":367,"mouseY":226,"timestamp":1484041786007,"event":"mousemove"},{"mouseX":259,"mouseY":203,"timestamp":1484041786107,"event":"mousemove"},{"mouseX":260,"mouseY":166,"timestamp":1484041786207,"event":"mousemove"},{"mouseX":320,"mouseY":131,"timestamp":1484041786307,"event":"mousemove"},{"mouseX":317,"mouseY":114,"timestamp":1484041786607,"event":"mousemove"},{"mouseX":309,"mouseY":109,"timestamp":1484041786707,"event":"mousemove"},{"mouseX":307,"mouseY":108,"timestamp":1484041786807,"event":"mousemove"},{"mouseX":306,"mouseY":106,"timestamp":1484041786907,"event":"mousemove"}]}

	data = data['data']

	instance= Mouse(data=data)

	print instance.angles()

	
