import sys

sys.path.append('../')

from server import models

sys.path.append('../../')
from lib import Behave, Keyboard, Mouse

import numpy as np
import matplotlib.pyplot as plt

users = models.Collect.query.all()

checkingID = 5

user = users[checkingID]

keyboard_instance_1 = Keyboard(data=user.dataChunk1)
keyboard_instance_2 = Keyboard(data=user.dataChunk2)
keyboard_instance_3 = Keyboard(data=user.dataChunk3)

mouse_instance_1 = Mouse(data=user.mouseDataChunk1)
mouse_instance_2 = Mouse(data=user.mouseDataChunk2)
mouse_instance_3 = Mouse(data=user.mouseDataChunk3)

def visualize_delay_durations():
	test_1 = plt.plot(range(len(keyboard_instance_1.delay_durations())), keyboard_instance_1.delay_durations())
	test_2 = plt.plot(range(len(keyboard_instance_2.delay_durations())), keyboard_instance_2.delay_durations())
	test_3 = plt.plot(range(len(keyboard_instance_3.delay_durations())), keyboard_instance_3.delay_durations())

	plt.setp(test_1, linewidth=0.5, color='r')
	plt.setp(test_2, linewidth=0.5, color='b')
	plt.setp(test_3, linewidth=0.5, color='g')

	plt.yscale('linear')
	plt.title('Delay Durations')
	plt.show()

def visualize_keystroke_rates():
	test_1 = plt.plot(range(len(keyboard_instance_1.keystroke_rates())), keyboard_instance_1.keystroke_rates())
	test_2 = plt.plot(range(len(keyboard_instance_2.keystroke_rates())), keyboard_instance_2.keystroke_rates())
	test_3 = plt.plot(range(len(keyboard_instance_3.keystroke_rates())), keyboard_instance_3.keystroke_rates())

	plt.setp(test_1, linewidth=0.5, color='r')
	plt.setp(test_2, linewidth=0.5, color='b')
	plt.setp(test_3, linewidth=0.5, color='g')

	plt.yscale('linear')
	plt.title('Keystroke Rates')
	plt.show()

def visualize_mouse_movespeed():
	test_1 = plt.plot(range(len(mouse_instance_1.move_speed())), mouse_instance_1.move_speed())
	test_2 = plt.plot(range(len(mouse_instance_2.move_speed())), mouse_instance_2.move_speed())
	test_3 = plt.plot(range(len(mouse_instance_3.move_speed())), mouse_instance_3.move_speed())

	plt.setp(test_1, linewidth=0.5, color='r')
	plt.setp(test_2, linewidth=0.5, color='b')
	plt.setp(test_3, linewidth=0.5, color='g')

	plt.yscale('linear')
	plt.title('Mouse Movespeed')
	plt.show()

def visualize_mouse_angles():
	test_1 = plt.plot(range(len(mouse_instance_1.angles())), mouse_instance_1.angles())
	test_2 = plt.plot(range(len(mouse_instance_2.angles())), mouse_instance_2.angles())
	test_3 = plt.plot(range(len(mouse_instance_3.angles())), mouse_instance_3.angles())

	plt.setp(test_1, linewidth=0.5, color='r')
	plt.setp(test_2, linewidth=0.5, color='b')
	plt.setp(test_3, linewidth=0.5, color='g')

	plt.yscale('linear')
	plt.title('Mouse Angles')
	plt.show()

visualize_keystroke_rates()