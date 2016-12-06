# Test server that receives post data and saves it to files
#
#
# IMPORTANT:
# required argument when starting the script is the path where the files should be saved 
#
#
#

from flask import Flask, request
import os
import sys


FILES_PATH = "../data/user_typing_info"


app = Flask(__name__)



def encode_dict(d, codec='utf8'):

	ks = d.keys()

	for k in ks:

		val = d.pop(k)

		if isinstance(val, unicode):

			val = val.encode(codec)

		elif isinstance(val, dict):

			val = encode_dict(val, codec)

		if isinstance(k, unicode):

			k = k.encode(codec)

		d[k] = val

	return d


@app.route("/", methods=["POST"])
def home():

	print FILES_PATH

	files = os.listdir(FILES_PATH)

	json_request = encode_dict(request.json)

	max_index = 0

	for file in files:

		try: file_int = int(file)
		except ValueError: continue

		max_index = max(max_index, file_int)


	max_index += 1 

	file = open(FILES_PATH + "/" + str(max_index), "w")

	file.write(str(json_request))

	return "file is saved"


if __name__ == "__main__":

	FILES_PATH = sys.argv[1]

	app.run(debug=True)