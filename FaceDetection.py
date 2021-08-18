import cv2

class FaceDetection:
    def __init__(self):
        self.faceCascade = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')
    
    def detect(self, frame):
        grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.faceCascade.detectMultiScale(grayFrame, scaleFactor=1.5, minNeighbors=5)
        return faces
