import cv2
from Camera import Camera
from MovimentDetection import MovimentDetection
from ObjectDetection import ObjectDetection
from FaceDetection import FaceDetection
from TimerProcess import TimerProcess
from TelegramBot import TelegramBot
import Rectangles
from threading import Thread
import time


def showFrame(frame):
    cv2.imshow('camera frame', frame)


def waitKeyPress():
    return cv2.waitKey(1)


def selectRectangleForMinArea(frame):
    global movimentDetection
    rect = cv2.selectROI(frame)
    area = Rectangles.calculateArea(rect)
    movimentDetection.objectMinArea = area
    cv2.destroyAllWindows()


def recognizeMovingObjects(frame, objectNames):
    global movimentDetection
    global objectDetection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    objects, rectangles = movimentDetection.getMovimentObjects(gray)
    detectedMovingObjects = []
    if (rectangles):
        biggestRect = Rectangles.getBiggest(rectangles)
        
        expandedRectangle = Rectangles.expand(biggestRect, 100)
        objectImage = Rectangles.getImage(expandedRectangle, frame)
        detectedObjects = objectDetection.detect(objectImage)
        for detectedObject in detectedObjects:
            label, rect, id = detectedObject
            if (label in objectNames):
                detectedMovingObjects.append((label, expandedRectangle, id))
        
    return detectedMovingObjects


def detectObjects(frame):
    global objectDetection
    detectedObjects = objectDetection.detect(frame)
    for detectedObject in detectedObjects:
        label, rect, id = detectedObject
        Rectangles.draw([rect], frame)
        cv2.putText(frame, label, (rect[0], rect[1] + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)


def detectFaces(frame):
    global faceDetection
    detectedFaces = faceDetection.detect(frame)
    for detectedFace in detectedFaces:
        objectImage = Rectangles.getImage(detectedFace, frame)
        Rectangles.draw([detectedFace], frame)
        cv2.imshow("detected face", objectImage)


def addDataToTimer(data):
    global timerProcess
    if (timerProcess == None):
        timerProcess = TimerProcess(5)

    timerProcess.addData(data)


def checkMovingObjects(data):
    global idleTimerProcess
    labels = [x[0] for x in data]
    distinctLabels = list(set(labels))

    for label in distinctLabels:
        labelsImgs = [x[2] for x in data if x[0] == label]
        if (len(labelsImgs) > 20):
            biggestImg = Rectangles.getBiggestImage(labelsImgs)
            cv2.imwrite("sendimage.jpg", biggestImg)
            telegramBot.sendPhoto(telegramChatId, "sendimage.jpg")
            idleTimerProcess = TimerProcess(15)

            # for img in labelsImgs:
            #  cv2.imshow("biggest image", img)
            # cv2.waitKey(0)
            # cv2.imwrite("images/image" + str(labelsImgs.index(img)) + ".jpg", img)

            #biggestImg = Rectangles.getBiggestImage(labelsImgs)


def main():
    global idleTimerProcess
    global timerProcess
    camera = Camera(cameraInput)
    camera.openVideo()

    while(True):
        frame = camera.getFrame()
        frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        
        if (idleTimerProcess == None):
            objects = recognizeMovingObjects(
                frame, ["person", "car", "dog", "cat", "sheep"])

            for object in objects:
                label, rect, classId = object
                objectImg = Rectangles.getImage(rect, frame)
                addDataToTimer([label, rect, objectImg])
        elif (idleTimerProcess.isClosed()):
            idleTimerProcess = None

        if (timerProcess != None and timerProcess.isClosed()):
            timerData = timerProcess.getData()
            timerProcess = None
            # checkMovingObjects(timerData)
            thread = Thread(target=checkMovingObjects, args=(timerData, ))
            thread.start()
        
        showFrame(frame)
        pressedKey = waitKeyPress()
        if pressedKey == ord('q'):
            break

        if pressedKey == ord('s'):
            selectRectangleForMinArea(frame)

        if pressedKey == ord('p'):
            rect = cv2.selectROI(frame)
            cv2.destroyAllWindows()
            objectImage = Rectangles.getImage(rect, frame)
            cv2.imwrite('image.jpg', objectImage)

    cv2.destroyAllWindows()

telegramToken = "TELEGRAM-TOKEN"
telegramChatId = 0 # Id do chat do telegram
cameraInput = "rtsp://{user}:{password}@{ip}}/live/mpeg4"

movimentDetection = MovimentDetection()
movimentDetection.objectMinArea = 2500
movimentDetection.start()
objectDetection = ObjectDetection()
faceDetection = FaceDetection()
timerProcess = None
telegramBot = TelegramBot(telegramToken)
idleTimerProcess = None

if __name__ == '__main__':
    main()
