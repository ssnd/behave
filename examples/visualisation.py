# TODO:
# - visualization for each parameter
# - visual comparison between two users


# snippet to import the library without relative routes
import sys, os
sys.path.insert(0, os.path.abspath("../.."))


from behave.lib import Behave

file = open("../data/user_typing_info/1", "r")
contents = file.read()

instance = Behave(contents)

print instance.keypress_delay_average()










