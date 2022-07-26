import cv2
from tensorflow.keras.models import load_model
import imutils
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('-i','--image',required=True)
args = vars(ap.parse_args())

model = load_model('model.hdf5')
labels = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F',
'G','H','I','J','K','L','M','N','P','Q','R','S','T','U','V','W','X','Y','Z']

image = cv2.imread(args['image'])

clone = image.copy()
clone = cv2.resize(clone,(300,600))
image = cv2.resize(image,(32,32))
image = img_to_array(image)
images = np.array([image])


pred = model.predict(images).argmax(axis=1)
cv2.putText(clone, f'Character: {labels[pred[0]]}', (10,30), cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
cv2.imshow('Number',clone)
cv2.waitKey(0)
