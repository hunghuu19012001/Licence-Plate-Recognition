import cv2
import imutils
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model


labels = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F',
'G','H','I','J','K','L','M','N','P','Q','R','S','T','U','V','W','X','Y','Z']

model = load_model('model.hdf5')

def sort_contours(cnts):
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
        key=lambda b:b[1][0], reverse=False))
    return (cnts,boundingBoxes)

class SegmentChar:
    def __init__(self) -> None:
        self.plate = None
        self.listChar = None
        self.thresh = None


    def loadplate(self,plate):
        plate = cv2.resize(plate,(600,400))
        self.plate = plate

    def showplate(self):
        cv2.imshow('Plate',self.plate)
        cv2.waitKey(0)

    def segmentPlate(self):
        # xử lí ảnh biển số và tìm contour
        gray = cv2.cvtColor(self.plate,cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray,30,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)[1]
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        # sắp xếp các contour và boudingBox theo thứ tự trái sang phải
        cnts,boundingBoxes = sort_contours(cnts)
        boundingBoxesChar =[]

        # tìm những bouding box phù hợp và tính tổng chiều cao các bouding box
        sumh = 0
        for b in boundingBoxes:
            (x,y,w,h) = b
            if w > 10 and w< 200 and h >70 and h <300:
                boundingBoxesChar.append(b)
                sumh+=h

        # Nếu không cắt được biển số thì trả về False
        if len(boundingBoxes) == 0:
            return False
        
        # Tính chiều cao trung bình của tất cả các bouding box
        hchar = sumh / len(boundingBoxesChar)
        BoxChar = []

        # Lọc ra tất cả những bouding Box có chiều cao trung bình
        # Mục đích lọc những phần tử nhiễu nằm ở bên trong kí tự 
        for c in boundingBoxesChar:
            if c[3] > hchar-5:
                BoxChar.append(c)
        
        # trả về True nếu cắt biển số thành công
        self.listChar = BoxChar
        self.thresh = thresh
        return True
    
    def ReadCharPlate(self):
        numberPlate = []
        for box in self.listChar:
            (x,y,w,h) = box
            cropped = self.thresh[y-5:min(y+h+5,self.thresh.shape[0]),max(x-12,0):min(x+w+13,self.thresh.shape[1])]
            cropped = cv2.resize(cropped,(32,32))
            cropped = img_to_array(cropped)
            boxchar = np.expand_dims(cropped,axis=0)
            pred = model.predict(boxchar).argmax(axis=1)
            char = labels[pred[0]]
            numberPlate.append(char)
            cv2.putText(self.plate,char,(x,y-5),cv2.FONT_HERSHEY_COMPLEX,0.75,(0,0,255),2)
            cv2.rectangle(self.plate,(x,y),(x+w,y+h),(0,255,0),3)

        return numberPlate

    