from app import app
from app import db
from flask import request,jsonify
import os
import subprocess
import rocksdb
import uuid
import json

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/',methods=["POST"])
@app.route('/<string:filename>',methods=["GET"])
def index(filename = None):
	target = os.path.join(APP_ROOT,"files/")
	
	if(not os.path.isdir(target)):
		os.mkdir(target)
		
	if request.method == "POST":
		file = request.files['data']
		filename = file.filename
		destination = "".join([target,filename])
		file.save(destination)

		key = uuid.uuid4().hex
		db.put(key.encode(),filename.encode())
		
		json_string = {"script-id": str(key)}
		return jsonify(json_string)
	else:
		filename = db.get(filename.encode()).decode()
		destination = "".join([target,filename])
		p = subprocess.Popen(["python", destination], stdout=subprocess.PIPE)
		out, err = p.communicate()
		return out
