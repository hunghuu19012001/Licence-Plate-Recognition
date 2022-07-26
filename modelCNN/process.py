import cv2
import os 
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array


class LoadnPreprocess:
    def __init__(self, width,height):
        self.width = width
        self.height = height
    
    def load(self,paths,verbose = -1):
        data = []
        labels = []
        for (i,p) in enumerate(paths):
            image = cv2.imread(p)
            lb = p.split(os.path.sep)[-2]

            image = cv2.resize(image,(self.width,self.height),interpolation=cv2.INTER_AREA)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            image = img_to_array(image)

            data.append(image)
            labels.append(lb)

            if verbose > 0 and i > 0 and (i+1)%verbose ==0:
                print(f'Preprocessed {i+1} Label: {lb}')
        return (np.array(data), np.array(labels))
