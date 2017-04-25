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

		fig, ax = plt.subplots(1, figsize=[7,4])

		fig.subplots_adjust(bottom=0.15)

		rect = patches.Rectangle(
			(0,down_deviation), 
			len(release_to_release)+10 ,
			up_deviation-down_deviation, 
			linewidth=1,
			edgecolor="r",
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