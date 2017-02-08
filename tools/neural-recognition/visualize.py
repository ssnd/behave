import sys

sys.path.append('../')

from server import models

sys.path.append('../../')
from lib import Behave, Keyboard, Mouse

import numpy as np
import matplotlib.pyplot as plt

users = models.Collect.query.all()

checkingID = int(sys.argv[1])

user = users[checkingID]

keyboard_instance_1 = Keyboard(data=user.dataChunk1)
keyboard_instance_2 = Keyboard(data=user.dataChunk2)
keyboard_instance_3 = Keyboard(data=user.dataChunk3)

def visualize_delay_durations():
	test_1 = plt.plot(range(len(keyboard_instance_1.press_durations())), keyboard_instance_1.press_durations())
	test_2 = plt.plot(range(len(keyboard_instance_2.press_durations())), keyboard_instance_2.press_durations())
	test_3 = plt.plot(range(len(keyboard_instance_3.press_durations())), keyboard_instance_3.press_durations())

	plt.setp(test_1, linewidth=0.5, color='r')
	plt.setp(test_2, linewidth=0.5, color='b')
	plt.setp(test_3, linewidth=0.5, color='g')

	plt.yscale('linear')
	plt.title('Delay Durations')
	plt.show()

visualize_delay_durations()