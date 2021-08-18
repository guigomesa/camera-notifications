import cv2
from MovimentDetection import MovimentDetection

class Camera:
    def __init__(self, cameraInput):
        self.cameraInput = cameraInput
        self.video = None

    '''
    Retorna o video capture conforme a cameraInput informado
    '''
    def getVideoCapture(self):
        return cv2.VideoCapture(self.cameraInput)        

    '''
    Informa se a camera está aberta
    '''
    def isOpened(self):
        return self.video.isOpened()

    def close(self):
        self.video.release()

    '''
    Abre o stream do video
    '''
    def openVideo(self):
        self.video = self.getVideoCapture()
    
    '''
    Retorna o proximo frame do video
    '''
    def getFrame(self):
        if (not self.isOpened()):
            self.openVideo()

        ret, frame = self.video.read()
        return frame;
