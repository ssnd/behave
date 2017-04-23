"""

{
"id":  "000983a4-5f15-4084-b79b-2daaa6d8615c" ,
"keyCode":  "28" ,
"keyPress":  "1492147908036" ,
"keyRelease":  "1492147908155" ,
"keypressGroup_id":  "cbf1bd50-b784-4649-b340-b51aa0b5f53f" ,
"user_id":  "7d40aeba-b7c3-41df-b610-c575b6f88426"
}

keypressGroups -> {
"id":  "15a83f54-ca97-4ae0-ae96-34d80f99e9fb"
}

"""


import sys

from collections import defaultdict
sys.path.append('../')

import rethinkdb as r

import operator

sys.path.append('../../')
from lib import Behave, Keyboard, Mouse

r.connect("localhost", 28015).repl()

user_id_list = r.table("users").run()
user_list = []

for user_id in user_id_list:
	user_id = user_id["id"]

	user = {}

	user["user_keypresses"] = []

	for key_group in r.table("keypresses").filter(r.row["user_id"]==user_id).get_field("keypressGroup_id").distinct().run():
		key_group_chunk = [k for k in r.table("keypresses").filter(r.row["keypressGroup_id"] == key_group).run()]
		key_group_chunk.sort(key=operator.itemgetter("keyPress"))
		if len(key_group_chunk) > 2:
			user["user_keypresses"].append(key_group_chunk)
		
	user_list.append(user)

user_list.pop(1)

for user in user_list:
	print "--------USER----------------------------------------------------------"
	overall_keyboard_params = []

	for key_group in user["user_keypresses"]:
		keyboard_test_instance = Keyboard(data=key_group)
		keyboard_params = keyboard_test_instance.get_keyboard_params()
		overall_keyboard_params.append(keyboard_params)


	print overall_keyboard_params