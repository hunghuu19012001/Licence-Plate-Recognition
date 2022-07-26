import cv2
import imutils
import numpy as np

class LicencePlate:
    def __init__(self):
        self.image = None
        self.plate = None

    def load_image(self,image_path):
        self.image = cv2.imread(image_path)
        self.image = cv2.resize(self.image,(620,480))

    def show_image(self):
        cv2.imshow('Car', self.image)
        cv2.waitKey(0)

    def crop_plate(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.bilateralFilter(gray, 13, 15, 15)

        edged = cv2.Canny(blurred,30,200)
        cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if cnts is None:
            return None
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]
        screenCnt = None

        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c,0.02*peri, True)
            # area = cv2.contourArea(c)

            if len(approx) == 4: #and area <10000:
                screenCnt = approx
                break
        
        if screenCnt is None:
            return None
        mask = np.zeros_like(gray, np.uint8)
        cv2.drawContours(mask,[screenCnt],0,255,-1)

        (x,y) = np.where(mask == 255)
        (topX, topY) = (np.min(x), np.min(y))
        (botX, botY) = (np.max(x), np.max(y))

        plate = self.image[topX:botX+1, topY: botY+1]

        return plate
