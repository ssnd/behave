# TODO:
# - visualization for each parameter
# - visual comparison between two users

# keypress deltas
# space delays
# backspace count 
# 


# snippet to import the library without relative routes
import sys, os

sys.path.insert(0, os.path.abspath("../../"))

from lib import Behave
import matplotlib.pyplot as plt
from matplotlib import collections as mc
import matplotlib.font_manager as font_manager
import matplotlib.patches as patches
import numpy as np
from random import randint


sys.path.append("../../")
from lib.behave import Behave
from lib.old.keyboard import Keyboard
from lib.old.mouse import Mouse


sys.path.append("../")

from server.models import Collect


class Behave_Visualization:

	def  __init__(self):
		self.UPLOAD_FOLDER = "saved"
		self.values_color = "#165EA9"
		# self.edgecolor = "#010101"
		self.deviation_color = "#1B8ECE"
		path_bold = "fonts/segoe_bold.ttf"
		path_regular = "fonts/segoe_regular.ttf"
		path_semi = "fonts/segoe_light.ttf"

		self.bold = font_manager.FontProperties(fname=path_bold)
		self.semi = font_manager.FontProperties(fname=path_semi)
		self.regular = font_manager.FontProperties(fname=path_regular)
		

	def get_user_data(self, id, chunk_no=1, mouse=False):
		current_obj = Collect.query.all()[id]
		if (mouse==False):
			if (chunk_no==1):
				chunk=current_obj.dataChunk1
			if (chunk_no==2):
				chunk=current_obj.dataChunk2
			if (chunk_no==3):
				chunk=current_obj.dataChunk3
			if (chunk_no==4):
				chunk=current_obj.dataChunk4

		if (mouse==True):
			if (chunk_no==1):
				chunk=current_obj.mouseDataChunk1
			if (chunk_no==2):
				chunk=current_obj.mouseDataChunk2
			if (chunk_no==3):
				chunk=current_obj.mouseDataChunk3
			if (chunk_no==4):
				chunk=current_obj.mouseDataChunk4



		current_obj_json = current_obj.get_json_data(chunk)

		return current_obj_json


	def dwell_flight_params(self):

		data = [{"keycode":77,"timestamp":1487170467448,"key_duration":86},{"keycode":82,"timestamp":1487170468098,"key_duration":71},{"keycode":32,"timestamp":1487170468718,"key_duration":55},{"keycode":68,"timestamp":1487170469470,"key_duration":98},{"keycode":85,"timestamp":1487170469968,"key_duration":91},{"keycode":82,"timestamp":1487170470465,"key_duration":80},{"keycode":83,"timestamp":1487170471478,"key_duration":103},{"keycode":76,"timestamp":1487170472055,"key_duration":87},{"keycode":69,"timestamp":1487170472855,"key_duration":84},{"keycode":89,"timestamp":1487170473398,"key_duration":90},{"keycode":32,"timestamp":1487170473745,"key_duration":67},{"keycode":87,"timestamp":1487170474311,"key_duration":84},{"keycode":65,"timestamp":1487170474705,"key_duration":89},{"keycode":83,"timestamp":1487170475128,"key_duration":89},{"keycode":32,"timestamp":1487170475578,"key_duration":67},{"keycode":84,"timestamp":1487170476335,"key_duration":67},{"keycode":72,"timestamp":1487170476939,"key_duration":68}]

		lines = []

		first_timestamp = data[0]['timestamp']
		first_duration = data[0]['key_duration']
		fig, ax = plt.subplots(1, figsize=[7,4])

		fig.subplots_adjust(bottom=0.15)

		colors = []
		lines.append([(first_timestamp-first_duration, 1), (first_timestamp-first_duration, 0)])
		ax.annotate(r'$x_0$', xy=(first_timestamp-first_duration, 0),  xycoords='data',	
				arrowprops=dict(facecolor='black', shrink=0.05),
				horizontalalignment='right', verticalalignment='top',fontsize=10
			)

		colors.append((0, 0, 1, 1))


		for i in range(len(data[:8])):
			timestamp = data[i]['timestamp']
			duration = data[i]['key_duration']

			next_timestamp  = data[i+1]['timestamp']
			next_duration = data[i+1]['key_duration']

			lines.append([(timestamp-duration, 0),(timestamp, 0)])

			colors.append((1,0,0,1))
			lines.append([(timestamp,0), (timestamp, 1)])
			colors.append((0, 0, 1, 1))
			lines.append([(timestamp,1), (next_timestamp-next_duration, 1)])
			ax.annotate(r'$y_' + str(i) + '$', xy=(timestamp, 0),  xycoords='data',
				arrowprops=dict(facecolor='black', shrink=0.5),
				horizontalalignment='left', verticalalignment='top',fontsize=10
			)
			colors.append((0, 1, 0, 1))
			ax.annotate(r'$x_'+ str(i+1)+ '$', xy=(next_timestamp-next_duration, 0),  xycoords='data',
				horizontalalignment='right', verticalalignment='top',fontsize=10
			)

			lines.append([(next_timestamp-next_duration, 1), (next_timestamp-next_duration, 0)])
			colors.append((0, 0, 1, 1))


		c = np.array(colors)

		lc = mc.LineCollection(lines, colors=c)
		
		ax.add_collection(lc)
		ax.autoscale()
		ax.margins(0.1)

		ax.set_yticklabels(["", "down" ,"","","","","up"], fontsize=12, fontproperties=self.regular)
		ax.set_xticklabels(["","1 second","2 second","3 second","4 second","5 second","6 second", "7 second"], fontsize=8, fontproperties=self.regular)
		plt.title("Dwell & Flight time chart", fontproperties=self.bold, y=1.04)
		plt.ylabel("Button state", fontsize=12, fontproperties=self.semi)
		plt.xlabel("Time passed", fontsize=12, fontproperties=self.semi)

		plt.savefig(self.UPLOAD_FOLDER + "/dwell_flight_time" + "_" + str(id) + ".svg")


	def durations(self):
		data = [{"keycode":77,"timestamp":1487176804584,"key_duration":82},{"keycode":82,"timestamp":1487176804719,"key_duration":44},{"keycode":32,"timestamp":1487176804768,"key_duration":93},{"keycode":68,"timestamp":1487176804941,"key_duration":5},{"keycode":85,"timestamp":1487176805040,"key_duration":104},{"keycode":82,"timestamp":1487176805259,"key_duration":96},{"keycode":83,"timestamp":1487176805664,"key_duration":46},{"keycode":76,"timestamp":1487176805727,"key_duration":109},{"keycode":69,"timestamp":1487176805848,"key_duration":81},{"keycode":89,"timestamp":1487176805972,"key_duration":86},{"keycode":32,"timestamp":1487176806129,"key_duration":86},{"keycode":87,"timestamp":1487176806767,"key_duration":78},{"keycode":65,"timestamp":1487176807010,"key_duration":3},{"keycode":83,"timestamp":1487176807111,"key_duration":104},{"keycode":32,"timestamp":1487176807270,"key_duration":74},{"keycode":84,"timestamp":1487176807707,"key_duration":78},{"keycode":72,"timestamp":1487176807832,"key_duration":79},{"keycode":69,"timestamp":1487176807900,"key_duration":59},{"keycode":32,"timestamp":1487176808030,"key_duration":83},{"keycode":68,"timestamp":1487176808487,"key_duration":84},{"keycode":73,"timestamp":1487176808613,"key_duration":51},{"keycode":82,"timestamp":1487176808690,"key_duration":19},{"keycode":69,"timestamp":1487176808775,"key_duration":104},{"keycode":67,"timestamp":1487176808974,"key_duration":55},{"keycode":84,"timestamp":1487176809002,"key_duration":83},{"keycode":79,"timestamp":1487176809099,"key_duration":52},{"keycode":82,"timestamp":1487176809211,"key_duration":94},{"keycode":32,"timestamp":1487176809297,"key_duration":79},{"keycode":79,"timestamp":1487176810084,"key_duration":72},{"keycode":70,"timestamp":1487176810198,"key_duration":78},{"keycode":32,"timestamp":1487176810292,"key_duration":84},{"keycode":65,"timestamp":1487176810822,"key_duration":20},{"keycode":32,"timestamp":1487176810870,"key_duration":68},{"keycode":70,"timestamp":1487176811349,"key_duration":65},{"keycode":73,"timestamp":1487176811448,"key_duration":83},{"keycode":82,"timestamp":1487176811516,"key_duration":55},{"keycode":77,"timestamp":1487176811628,"key_duration":66},{"keycode":32,"timestamp":1487176811791,"key_duration":73},{"keycode":67,"timestamp":1487176812489,"key_duration":57},{"keycode":65,"timestamp":1487176812563,"key_duration":130},{"keycode":76,"timestamp":1487176812642,"key_duration":55},{"keycode":76,"timestamp":1487176812793,"key_duration":8},{"keycode":69,"timestamp":1487176812854,"key_duration":69},{"keycode":68,"timestamp":1487176813031,"key_duration":74},{"keycode":32,"timestamp":1487176813655,"key_duration":91},{"keycode":71,"timestamp":1487176814535,"key_duration":49},{"keycode":82,"timestamp":1487176814580,"key_duration":94},{"keycode":85,"timestamp":1487176814710,"key_duration":80},{"keycode":78,"timestamp":1487176814871,"key_duration":78},{"keycode":78,"timestamp":1487176815365,"key_duration":74},{"keycode":73,"timestamp":1487176815512,"key_duration":31},{"keycode":78,"timestamp":1487176815605,"key_duration":124},{"keycode":71,"timestamp":1487176815709,"key_duration":93},{"keycode":32,"timestamp":1487176815785,"key_duration":73},{"keycode":87,"timestamp":1487176816524,"key_duration":92},{"keycode":72,"timestamp":1487176816638,"key_duration":21},{"keycode":73,"timestamp":1487176816704,"key_duration":87},{"keycode":67,"timestamp":1487176816860,"key_duration":18},{"keycode":72,"timestamp":1487176816929,"key_duration":87},{"keycode":32,"timestamp":1487176817030,"key_duration":79},{"keycode":77,"timestamp":1487176817553,"key_duration":78},{"keycode":65,"timestamp":1487176817683,"key_duration":117},{"keycode":68,"timestamp":1487176817844,"key_duration":28},{"keycode":69,"timestamp":1487176817912,"key_duration":96},{"keycode":32,"timestamp":1487176818030,"key_duration":81},{"keycode":68,"timestamp":1487176818738,"key_duration":37},{"keycode":82,"timestamp":1487176818809,"key_duration":3},{"keycode":73,"timestamp":1487176818920,"key_duration":54},{"keycode":76,"timestamp":1487176818961,"key_duration":6},{"keycode":69,"timestamp":1487176819033,"key_duration":78},{"keycode":83,"timestamp":1487176819650,"key_duration":94},{"keycode":32,"timestamp":1487176820462,"key_duration":71},{"keycode":72,"timestamp":1487176820953,"key_duration":1},{"keycode":69,"timestamp":1487176821031,"key_duration":79},{"keycode":32,"timestamp":1487176821182,"key_duration":85},{"keycode":87,"timestamp":1487176821750,"key_duration":79},{"keycode":65,"timestamp":1487176821916,"key_duration":7},{"keycode":83,"timestamp":1487176822004,"key_duration":95},{"keycode":32,"timestamp":1487176822088,"key_duration":68},{"keycode":65,"timestamp":1487176822681,"key_duration":80},{"keycode":32,"timestamp":1487176822765,"key_duration":78},{"keycode":66,"timestamp":1487176823160,"key_duration":64},{"keycode":73,"timestamp":1487176823296,"key_duration":33},{"keycode":71,"timestamp":1487176823371,"key_duration":108},{"keycode":32,"timestamp":1487176823499,"key_duration":75},{"keycode":66,"timestamp":1487176824229,"key_duration":78},{"keycode":69,"timestamp":1487176824286,"key_duration":54},{"keycode":69,"timestamp":1487176824480,"key_duration":3},{"keycode":70,"timestamp":1487176824581,"key_duration":104},{"keycode":89,"timestamp":1487176824800,"key_duration":84},{"keycode":32,"timestamp":1487176824963,"key_duration":63},{"keycode":77,"timestamp":1487176825526,"key_duration":67},{"keycode":65,"timestamp":1487176825630,"key_duration":96},{"keycode":78,"timestamp":1487176825706,"key_duration":67},{"keycode":32,"timestamp":1487176825875,"key_duration":68},{"keycode":87,"timestamp":1487176826516,"key_duration":5},{"keycode":73,"timestamp":1487176826592,"key_duration":81},{"keycode":84,"timestamp":1487176826714,"key_duration":23},{"keycode":72,"timestamp":1487176826740,"key_duration":49},{"keycode":32,"timestamp":1487176826974,"key_duration":81},{"keycode":65,"timestamp":1487176827529,"key_duration":28},{"keycode":72,"timestamp":1487176827602,"key_duration":101},{"keycode":82,"timestamp":1487176827678,"key_duration":58},{"keycode":68,"timestamp":1487176827923,"key_duration":5},{"keycode":76,"timestamp":1487176827991,"key_duration":73},{"keycode":69,"timestamp":1487176828293,"key_duration":71},{"keycode":89,"timestamp":1487176828399,"key_duration":46},{"keycode":32,"timestamp":1487176828871,"key_duration":43},{"keycode":65,"timestamp":1487176829485,"key_duration":21},{"keycode":78,"timestamp":1487176829533,"key_duration":69},{"keycode":68,"timestamp":1487176829631,"key_duration":52},{"keycode":89,"timestamp":1487176829756,"key_duration":52},{"keycode":32,"timestamp":1487176830040,"key_duration":96},{"keycode":78,"timestamp":1487176830767,"key_duration":112},{"keycode":69,"timestamp":1487176830845,"key_duration":73},{"keycode":67,"timestamp":1487176830981,"key_duration":100},{"keycode":74,"timestamp":1487176831059,"key_duration":50},{"keycode":32,"timestamp":1487176831517,"key_duration":95},{"keycode":65,"timestamp":1487176831922,"key_duration":31},{"keycode":76,"timestamp":1487176831981,"key_duration":90},{"keycode":71,"timestamp":1487176832120,"key_duration":25},{"keycode":79,"timestamp":1487176832186,"key_duration":91},{"keycode":84,"timestamp":1487176832339,"key_duration":31},{"keycode":72,"timestamp":1487176832394,"key_duration":86},{"keycode":32,"timestamp":1487176832541,"key_duration":77}]



		instance = Keyboard(data=data)

		durations = instance.durations

		average = instance.average(durations)

		deviation = instance.standart_deviation(durations)

		x_values = [i for i in range(len(durations))]

		averages = [average for i in durations]

		up_deviation = average+deviation

		down_deviation = average-deviation

		fig, ax = plt.subplots(1, figsize=[7,4])

		fig.subplots_adjust(bottom=0.15)

		rect = patches.Rectangle(
			(0,down_deviation), 
			len(durations)+10 ,
			up_deviation-down_deviation, 
			linewidth=1,
			edgecolor=self.deviation_color,
			facecolor=self.deviation_color,
			fill=True,
			alpha=0.4,
			label="Deviation range"
		)

		rect1 = patches.Rectangle(
			(0,up_deviation), 
			len(durations)+10 ,
			max(durations), 
			linewidth=1,
			edgecolor='g',
			facecolor='g',
			fill=True,
			alpha=0.4,
			label="Time between words"
		)


		ax.plot(x_values, durations, "o-", 
				label="Parameter value", 
				color=self.values_color)

		ax.plot(x_values, averages, linewidth=2, label="Average", color=self.values_color)
		ax.add_patch(rect)
		ax.add_patch(rect1)

		# fig.ylim[x_values[0], x_values[len(x_values)-1]]

		plt.title("Flight time chart", fontproperties=self.bold, y=1.04)

		plt.ylabel("Flight time", fontproperties=self.semi)

		plt.xlabel("Press count", fontproperties=self.semi)
		
		axes = plt.gca()

		legend = ax.legend(loc="lower right", shadow=False, framealpha=0.5, prop=self.regular)

		axes.set_xlim([x_values[0], x_values[len(x_values)-1]])

		plt.savefig(self.UPLOAD_FOLDER + "/durations" + "_" + str(id) + ".svg")
		

	def release_to_release(self, id):

		data = self.get_user_data(id)

		instance = Keyboard(data=data)

		release_to_release = instance.release_to_release()

		release_to_release = release_to_release['_letter']

		average = instance.average(release_to_release)

		deviation = instance.standart_deviation(release_to_release)

		x_values = [i for i in range(len(release_to_release))]

		averages = [average for i in release_to_release]

		up_deviation = average+deviation

		down_deviation = average-deviation

		fig, ax = plt.subplots(1)

		fig.subplots_adjust(bottom=0.15)

		rect = patches.Rectangle(
			(0,down_deviation), 
			len(release_to_release)+10 ,
			up_deviation-down_deviation, 
			linewidth=1,
			edgecolor=None,
			facecolor=self.deviation_color,
			fill=True,
			alpha=0.5,
			hatch="\\\\",
			label="Deviation range"
		)

		ax.plot(x_values, release_to_release, "o-", 
				label="Parameter value", 
				color=self.values_color)

		ax.plot(x_values, averages, linewidth=2, label="Average", color=self.values_color)

		ax.add_patch(rect)

		plt.title("Release-to-Release time chart", fontproperties=self.bold, y=1.04)

		plt.ylabel("Release-to-Release time", fontproperties=self.semi)

		plt.xlabel("Press count", fontproperties=self.semi)

		axes = plt.gca()

		legend = ax.legend(loc="lower right", shadow=False, framealpha=0.5, prop=self.regular)

		axes.set_xlim([x_values[0], x_values[len(x_values)-1]])

		plt.savefig(self.UPLOAD_FOLDER + "/release_to_release" + "_" + str(id) + ".svg")



	def press_to_press(self, id):

		data = self.get_user_data(id)

		instance = Keyboard(data=data)

		press_to_press = instance.press_to_press()

		press_to_press = press_to_press['_letter']

		average = instance.average(press_to_press)

		deviation = instance.standart_deviation(press_to_press)

		x_values = [i for i in range(len(press_to_press))]

		averages = [average for i in press_to_press]

		up_deviation = average+deviation

		down_deviation = average-deviation

		fig, ax = plt.subplots(1)

		fig.subplots_adjust(bottom=0.15)

		rect = patches.Rectangle(
			(0,down_deviation), 
			len(press_to_press)+10 ,
			up_deviation-down_deviation, 
			linewidth=1,
			edgecolor=self.deviation_color,
			facecolor=self.deviation_color,
			fill=True,
			alpha=0.5,
			hatch="\\\\",
			label="Deviation range"
		)

		ax.plot(x_values, press_to_press, "o-", 
				label="Parameter value", 
				color=self.values_color)

		ax.plot(x_values, averages, linewidth=2, label="Average", color=self.values_color)

		ax.add_patch(rect)

		legend = ax.legend(loc="lower right", shadow=False, prop=self.regular, framealpha=0.5)

		# fig.ylim[x_values[0], x_values[len(x_values)-1]]

		plt.title("Press-to-Press time chart", fontproperties=self.bold, y=1.04)

		plt.ylabel("Press-to-Press time", fontproperties=self.semi)

		plt.xlabel("Press count", fontproperties=self.semi)
		
		axes = plt.gca()

		axes.set_xlim([x_values[0], x_values[len(x_values)-1]])

		plt.savefig(self.UPLOAD_FOLDER + "/press_to_press" + "_" + str(id) + ".svg")


	def flight(self, id):

		data = self.get_user_data(id)

		instance = Keyboard(data=data)

		flight_time = instance.flight_time()

		flight_time = flight_time['_letter']

		average = instance.average(flight_time)

		deviation = instance.standart_deviation(flight_time)

		fig, ax = plt.subplots(1)

		fig.subplots_adjust(bottom=0.15)

		x_values = [i for i in range(len(flight_time))]

		averages = [average for i in flight_time]

		up_deviation = average+deviation

		down_deviation = average-deviation


		rect = patches.Rectangle(
			(0,down_deviation), 
			len(flight_time)+10 ,
			up_deviation-down_deviation, 
			linewidth=1,
			edgecolor=self.deviation_color,
			facecolor=self.deviation_color,
			fill=True,
			alpha=0.5,
			hatch="\\\\",
			label="Deviation range"
		)



		ax.plot(x_values, flight_time, "o-", label="Parameter value", color=self.values_color)

		ax.plot(x_values, averages, linewidth=2, label="Average",  color=self.values_color)

		ax.add_patch(rect)

		legend = ax.legend(loc="lower right", shadow=False, framealpha=0.5, prop=self.regular)


		# fig.ylim[x_values[0], x_values[len(x_values)-1]]

		plt.title("Flight time chart", fontproperties=self.bold, y=1.04)

		plt.ylabel("Flight time", fontproperties=self.semi)

		plt.xlabel("Press count", fontproperties=self.semi)
		
		axes = plt.gca()

		axes.set_xlim([x_values[0], x_values[len(x_values)-1]])

		plt.savefig(self.UPLOAD_FOLDER + "/flight" + "_" + str(id) + ".svg")

	def dwell(self, id):

		data = self.get_user_data(id)

		instance = Keyboard(data=data)

		dwell_time = instance.dwell_time()

		average = instance.average(dwell_time)

		deviation = instance.standart_deviation(dwell_time)

		print deviation
		x_values = [i for i in range(len(dwell_time))]

		averages = [average for i in dwell_time]

		up_deviation = average+deviation

		down_deviation = average-deviation

		fig, ax = plt.subplots(1)

		fig.subplots_adjust(bottom=0.15)



		rect = patches.Rectangle(
			(0,down_deviation), 
			len(dwell_time)+10 ,
			up_deviation-down_deviation, 
			linewidth=1,
			edgecolor=self.deviation_color,
			facecolor=self.deviation_color,
			fill=True,
			alpha=0.5,
			hatch="\\\\",
			label="Deviation range"
		)


		ax.plot(x_values, dwell_time, "o-", 
				label="Parameter value", 
				color=self.values_color)

		ax.plot(x_values, averages, linewidth=2, label="Average", color=self.values_color)

		ax.add_patch(rect)

		legend = ax.legend(loc="lower right", shadow=False, framealpha=0.5, prop=self.regular)

		# fig.ylim[x_values[0], x_values[len(x_values)-1]]

		plt.title("Dwell time chart", fontproperties=self.bold, y=1.04)

		plt.ylabel("dwell time", fontproperties=self.semi)

		plt.xlabel("Press count", fontproperties=self.semi)

		axes = plt.gca()

		axes.set_xlim([x_values[0], x_values[len(x_values)-1]])

		# axes.set_ylim(max(dwell_time)+10, min(dwell_time)-10)

		plt.savefig(self.UPLOAD_FOLDER + "/dwell" + "_" + str(id) + ".svg")

	def mouse_speed(self, id):

		data = self.get_user_data(id, mouse=True)

		instance = Mouse(data=data)

		move_speed = instance.move_speed()

		average = instance.average(move_speed)

		deviation = instance.standart_deviation(move_speed)

		x_values = [i for i in range(len(move_speed))]

		averages = [average for i in move_speed]

		up_deviation = average+deviation

		down_deviation = average-deviation

		fig, ax = plt.subplots(1)

		fig.subplots_adjust(bottom=0.15)

		rect = patches.Rectangle(
			(0,down_deviation), 
			len(move_speed)+10 ,
			up_deviation-down_deviation, 
			linewidth=1,
			edgecolor=self.deviation_color,
			facecolor=self.deviation_color,
			fill=True,
			alpha=0.5,
			hatch="\\\\",
			label="Deviation range"
		)

		ax.plot(x_values, move_speed, "o-", 
				label="Parameter value", 
				color=self.values_color)

		ax.plot(x_values, averages, linewidth=2, label="Average", color=self.values_color)

		ax.add_patch(rect)

		plt.title("Mouse speed chart", fontproperties=self.bold, y=1.04)

		plt.ylabel("mouse speed time", fontproperties=self.semi)

		plt.xlabel("Tracking time", fontproperties=self.semi)

		legend = ax.legend(loc="lower right", shadow=False, framealpha=0.5, prop=self.regular)

		axes = plt.gca()

		axes.set_xlim([x_values[0], x_values[len(x_values)-1]])
		axes.set_ylim(min(move_speed)-0.1, max(move_speed)+0.1)

		plt.savefig(self.UPLOAD_FOLDER + "/mouse_speed" + "_" + str(id) + ".svg")








if __name__ == "__main__":
	Behave_Visualization().dwell_flight_params()
	# Behave_Visualization().press_to_press(2)
	# Behave_Visualization().release_to_release(1)
	# Behave_Visualization().flight(2)
	# Behave_Visualization().mouse_speed(2)


# print instance.keypress_delay_average()

