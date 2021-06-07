from __future__ import print_function
import requests
import json
import cv2
import pyttsx3
engine = pyttsx3.init()

file_name = "trial.jpg"
addr = 'http://localhost:5000'
test_url = addr + '/api/test'

content_type = 'image/jpeg'
headers = {'content-type': content_type}

img = cv2.imread(file_name)
_, img_encoded = cv2.imencode('.jpg', img)
response = requests.post(test_url, data=img_encoded.tostring(), headers=headers)
caption = json.loads(response.text)["caption"]
print(caption)

engine.say(caption)
engine.runAndWait()