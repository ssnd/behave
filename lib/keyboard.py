from behave import Behave
import ast, os, math
class Keyboard(Behave):
	"""Instance of the Behave class. Gathers the keystroke dynamics information.

	Example:
		instance = Keyboard(data)

		delay_durations= instance.delay_durations()
		print instance.standart_deviation(delay_durations)
		>>> 73.2461603089

		print instance.average(delay_durations)
 	"""
	def __init__(self, data):
		"""
		Args:
			data (Array): Array containing the following information about each keystroke:
				[
				...,
				{
					"keyPress" : ..., # unix timestamp of the press time
					"keyRelease" : ... , # unix timestamp of the release time
					"keyCode" : ... # ascii code of the key that was pressed
				},
				...
				]
		"""
		Behave.__init__(self, data)

		self.data = data
		
		if (type(data) == str):
			self.data = ast.literal_eval(data)

		self.key_press_arr = []
		self.key_release_arr = []
		self.key_code_arr = []

		for keystroke in self.data:

			key_press = keystroke['keyPress']

			key_release = keystroke['keyRelease']

			key_code = keystroke['keyCode']

			if "keyPress" in keystroke and key_press != None and key_release != None and key_code != None:
				self.key_press_arr.append(int(key_press))
				self.key_release_arr.append(int(key_release))
				self.key_code_arr.append(str(key_code))



	@staticmethod 
	def letter_filter(unfiltered_arr):
		"""Static method. 
		Return only keypress events where letters were typed.
		
		Args:
		    unfiltered_arr (Array): Input array containing keypress information
		
		Returns:
		    Array: Filtered array
		"""

		return [k for k in unfiltered_arr if len(k["keyCode"])==1]

	@staticmethod
	def keyname_filter(unfiltered_arr, keyname_str):
		"""Return only events where keycode equals to keyname_str
		
		Args:
		    unfiltered_arr (Array): Input array with keypress events
		    keyname_str (String): Keycode number to filter by
		
		Returns:
		    Array: Filtered array
		"""

		return [k for k in unfiltered_arr if k["keyCode"]==keyname_str]

	def dwell_time(self):
		"""Return an array of keypress durations

		Returns:
			Array: Ouput array
		"""

		press_durations_arr = [self.key_release_arr[i] - self.key_press_arr[i] for i in range(len(self.key_press_arr))]

		return press_durations_arr

	def flight_time(self):
		"""Return an array of delays between previous key release and next keypress.
		
		Returns:
			Array: Array of delays.
		"""
		flight_time_arr = []

		for i in range(0, len(self.key_press_arr) - 1):
			previous_release = self.key_release_arr[i]
			next_press = self.key_press_arr[i+1]
			flight_time = next_press - previous_release
			flight_time_arr.append(flight_time)

		return flight_time_arr

	def press_to_press(self):
		"""Return an array of delays between keypresses.
		
		Returns:
			Array: Array of delays.
		"""
		press_to_press_arr = []

		for i in range(0, len(self.key_press_arr) - 1):
			previous_press = self.key_press_arr[i]
			next_press = self.key_press_arr[i+1]
			press_to_press = next_press - previous_press
			press_to_press_arr.append(press_to_press)

		return press_to_press_arr

	def release_to_release(self):
		"""Return an array of delays between key releases.
		
		Returns:
			Array: Array of delays.
		"""
		release_to_release_arr = []

		for i in range(0, len(self.key_press_arr) - 1):
			previous_release = self.key_release_arr[i]
			next_release = self.key_release_arr[i+1]
			release_to_release = next_release - previous_release
			release_to_release_arr.append(release_to_release)

		return release_to_release_arr

	def get_keyboard_params(self):
		"""
		Returns an array of all analyzed values as a dictionary
		"""

		val_arr = {}

		letter_instance = Keyboard(data=self.letter_filter(self.data))

		val_arr['dwell_time_average'] = self.average(letter_instance.dwell_time())
		val_arr['flight_time_average'] = self.average([k for k in letter_instance.flight_time() if k < 700])
		val_arr['rtor_time_average'] = self.average([k for k in letter_instance.release_to_release() if k < 700])
		val_arr['ptop_time_average'] = self.average([k for k in letter_instance.press_to_press() if k < 700])

		#self.key

		#val_arr['space_dwell_time_average'] = self.average(self.dwell_time())

		#val_arr['dwell_time_std'] = self.standart_deviation(self.dwell_time())
		#val_arr['flight_time_std'] = self.standart_deviation(self.flight_time())
		#val_arr['rtor_time_std'] = self.standart_deviation(self.release_to_release())
		#val_arr['ptop_time_std'] = self.standart_deviation(self.press_to_press())

		return val_arr