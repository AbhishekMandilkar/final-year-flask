from cProfile import label
from importlib.resources import path
import json
import os
import cv2
import numpy as np
from flask import Flask, flash, jsonify
from flask import request

# flask config
app = Flask(__name__)
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True

#yolo config
net = cv2.dnn.readNet('./models/yolov4-custom_last.weights', './models/yolov4-custom.cfg')
classes = []
with open("./classes.txt", "r") as f:
    classes = f.read().splitlines()
colors = np.random.uniform(0, 255, size=(100, 3))

# uploads config
UPLOAD_FOLDER = './images/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#file validation
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


    

# main route
@app.route("/",methods=['GET','POST'])
def home():
    if request.method == 'GET':
        # get 
        return "Hello World"

    if request.method == 'POST':
        # post
        # app.logger.debug('Headers: %s', request.files)
        if request.files:
            img = request.files['image']
            app.logger.info('function is about to hit %s')
            img.save(os.path.join(app.config['UPLOAD_FOLDER'], img.filename))
            path = "./images/"+img.filename
            label = modelRunner(path)
            if len(label) > 0:
                print("label",label)
                return jsonify({"status": 1, "label": label})
            else:
                print("labelnot done")
                return jsonify({"status":0,"message":"No label found"})
        else:
            return "no file"








# model runner
def modelRunner(image):
    app.logger.info('function is hit %s')
    print(image)
    img = cv2.imread(image)
    height, width, channels = img.shape
    print( height, width, channels)
    # _, img = image
    # height, width, _ = img.shape
    blob = cv2.dnn.blobFromImage(img, 1/255, (416, 416), (0,0,0), swapRB=True, crop=False)
    net.setInput(blob)
    output_layers_names = net.getUnconnectedOutLayersNames()
    layerOutputs = net.forward(output_layers_names)
    
    boxes = []
    confidences = []
    class_ids = []

    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.1:
                center_x = int(detection[0]*width)
                center_y = int(detection[1]*height)
                w = int(detection[2]*width)
                h = int(detection[3]*height)

                x = int(center_x - w/2)
                y = int(center_y - h/2)

                boxes.append([x, y, w, h])
                print("confidence ",float(confidence))
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.2, 0.3)
  
    
    label = ""
    if len(indexes)>0:
        print("hi from condition")
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = str(round(confidences[i],2))
            color = colors[i]
            cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)

    return label     

    
        