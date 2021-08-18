import cv2
import json
import Rectangles

class ObjectDetection:
    def __init__(self):
        self.configurationFile = 'mobilenet_v3_large.pbtxt'
        self.frozenModel = 'frozen_inference_graph.pb'
        with open('mobilenet_v3_large_labels.json') as json_file:
            self.labelsData = json.load(json_file)
        self.start()    

    def start(self):
        self.model = cv2.dnn_DetectionModel(self.frozenModel, self.configurationFile)
        self.model.setInputSize(320,320)
        self.model.setInputScale(1.0/127.5)
        self.model.setInputMean((127.5, 127.5, 127.5))
        self.model.setInputSwapRB(True)    
    
    def getLabelName(self, index):
        label = [x for x in self.labelsData if x["id"] == index]
        if (not label):
            return "Unknow";

        return label[0]["display_name"]

    def detect(self, img):

        classIndex, confidence, bbox = self.model.detect(img, confThreshold=0.5) 
        detections = []

        if classIndex is None or type(classIndex) is tuple:
            return detections

        for classId, confidence, box in zip(classIndex.flatten(),confidence.flatten(), bbox):
            if (confidence > 0.65):
                detections.append([self.getLabelName(classId), box, classId])

        return detections;

def test():
    objectDetection = ObjectDetection()
    labelPerson = objectDetection.getLabelName(1)
    if (labelPerson != "person"):
        raise Exception("label name of index 1 should be person");              

    labelPerson = objectDetection.getLabelName(18)
    if (labelPerson != "dog"):
        raise Exception("label name of index 18 should be dog");                      

    labelPerson = objectDetection.getLabelName(1000)
    if (labelPerson != "Unknow"):
        raise Exception("unknow label name should be Unknow");                              

    print("all test passed")

test()        