import sys

sys.path.append('../')

from server import models

sys.path.append('../../')
from lib import Behave, Keyboard, Mouse

users = models.Collect.query.all()

keyboard_test_data = users[int(sys.argv[1])].dataChunk3

keyboard_test_instance = Keyboard(data=keyboard_test_data)

for c in keyboard_test_instance.press_to_press(): print c

print "DEVIATION: ", keyboard_test_instance.standart_deviation(keyboard_test_instance.press_to_press())