from flask import Flask, request, jsonify
import lpr
import cv2
from PIL import Image
import io
import numpy as np

platedetector = lpr.LPR(modelConfiguration="./WEIGHTS/darknet-yolov3.cfg",modelWeights = "./WEIGHTS/lapi.weights")
charRecognizer = lpr.CR(modelFile='./WEIGHTS/character_recognition.h5')

app = Flask(__name__)
print("=======================\nSERVER INITIATED\n=======================\n")

@app.route('/')
def test():
    return test()


@app.route('/get_plate',methods=['POST'])
def get_plate():
	if(request.method == 'POST'):
		data = request.data		
		img = cv2.imdecode(np.fromstring(data,np.uint8),1)

		plate_coor = platedetector.detect_plate(img)
		plate_chars = charRecognizer.opencvReadPlate(img[plate_coor[0][0]:plate_coor[0][1],plate_coor[0][2]:plate_coor[0][3]])
		# print(plate_chars)
		return jsonify(plate_chars = plate_chars)
	else:
		return "400"
