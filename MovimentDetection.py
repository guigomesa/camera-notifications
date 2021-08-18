import Rectangles
import cv2

class MovimentDetection:
    def __init__(self):
        self.history = 1000
        self.varThreshold = 100
        self.rectanglesMinArea = 150
        self.objectMinArea = 1500

    def start(self):
        self.started = True
        self.backgroundSubtractor = cv2.createBackgroundSubtractorMOG2(
            history=self.history, varThreshold=self.varThreshold, detectShadows=True)

    def findContours(self, mask):
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return contours
   

    def getMovimentObjects(self, frame):
        if (not self.started):
            self.start()

        mask = self.backgroundSubtractor.apply(frame)
        
        contours = self.findContours(mask)
        rectangles = Rectangles.getByContours(contours, self.rectanglesMinArea)
        rectangles = Rectangles.merge(rectangles, self.objectMinArea)

        objects = []
        for rect in rectangles:
            x, y, w, h = rect;
            objects.append(frame[y:y+h, x:x+w])

        return objects, rectangles


