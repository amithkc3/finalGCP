from flask import Flask, request, jsonify
import lpr
import cv2
from PIL import Image
import io
import numpy as np
import json
import requests

platedetector = lpr.LPR(modelConfiguration="./WEIGHTS/darknet-yolov3.cfg",modelWeights = "./WEIGHTS/lapi.weights")
charRecognizer = lpr.CR(modelFile='./WEIGHTS/character_recognition.h5')

app = Flask(__name__)
print("=======================\nSERVER INITIATED\n=======================\n")

@app.route('/')
def test():
    return "hello"


@app.route('/get_plate_checkin',methods=['POST'])
def get_plate_checkin():
	if(request.method == 'POST'):
		data = request.data		
		img = cv2.imdecode(np.fromstring(data,np.uint8),1)

		plate_coor = platedetector.detect_plate(img)
		if(len(plate_coor)):
			plate_chars = charRecognizer.opencvReadPlate(img[plate_coor[0][0]:plate_coor[0][1],plate_coor[0][2]:plate_coor[0][3]])
		# print(plate_chars)
			plate_info = {"licenseNo" :plate_chars,"parking": '0001'}
			firebase_url_checkin = 'https://us-central1-final-year-project-d4c31.cloudfunctions.net/vehicleCheckIn'
			requests.post(firebase_url_checkin,json=json.dumps(plate_info))
			return jsonify(plate_info)
		else:
			return jsonify(licenseNo = '')
	else:
		return "400"

@app.route('/get_plate_checkout',methods=['POST'])
def get_plate_checkout():
	if(request.method == 'POST'):
		data = request.data		
		img = cv2.imdecode(np.fromstring(data,np.uint8),1)

		plate_coor = platedetector.detect_plate(img)
		if(len(plate_coor)):
			plate_chars = charRecognizer.opencvReadPlate(img[plate_coor[0][0]:plate_coor[0][1],plate_coor[0][2]:plate_coor[0][3]])
		# print(plate_chars)
			plate_info = {"licenseNo" :plate_chars,"parking": '0001'}
			firebase_url_checkout = 'https://us-central1-final-year-project-d4c31.cloudfunctions.net/vehicleCheckOut'
			requests.post(firebase_url_checkout,json=json.dumps(plate_info))
			return jsonify(plate_info)
		else:
			return jsonify(licenseNo = '')
	else:
		return "400"

@app.route('/dump_registered_plates',methods=['POST'])
def dump_registered_plates():
	if(request.method == 'POST'):
		data = request.get_json()	
		print(data)
		with open('registered_plates.json','w') as file:
			json.dump(data,file)
		return "200"
	else:
		return "400"


if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8000, debug=True)