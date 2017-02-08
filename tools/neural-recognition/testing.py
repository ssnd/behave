import sys

from collections import defaultdict
sys.path.append('../')

from server import models

sys.path.append('../../')
from lib import Behave, Keyboard, Mouse

users = models.Collect.query.all()


"""

RANGE - 4 - 24

25

2, 3, 7, 8, 9, 11, 12, 13, 15, 16, 17, 18, 19, 22
"""
userID = int(sys.argv[1])

user = users[userID]

keyChunks 	= [user.dataChunk1, user.dataChunk2, user.dataChunk3, user.dataChunk4]

paramsDict = defaultdict(list)

for keyboard_test_data in keyChunks:

	keyboard_test_instance = Keyboard(data=keyboard_test_data)

	test_data_to_normalize = keyboard_test_instance.get_keyboard_params()

	for key in test_data_to_normalize: paramsDict[key].append(test_data_to_normalize[key])

for i in paramsDict:
	print "PARAMETER:", i
	for j in paramsDict[i]: print j
	print "-----"