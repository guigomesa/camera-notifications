import pickle
import os

class CameraData:
    def __init__(self, name:str, cameraInput: str):
        self._cameraInput = cameraInput
        self._name = name
    
    @property
    def cameraInput(self):
        return self._cameraInput

    @property
    def name(self):
        return self._name


class CamerasData:
    def __init__(self):
        self.data : list[CameraData] = []

    def add(self, cameraData: CameraData) -> None:
        self.data.append(cameraData)

    def get(self, index) -> CameraData:
        return self.data[index]

    def getAll(self) -> list[CameraData]:
        return self.data

    def getCount(self) -> int:
        return len(self.data)

    def save(self, fileName: str) -> None:
        with open(fileName, 'wb') as file:
            pickle.dump(self, file)
    
    def load(fileName:str) -> 'CamerasData':
        if (not os.path.isfile(fileName)):
            return CamerasData()

        with open(fileName, 'rb') as file:
            return pickle.load(file) 

def test():
    camera1 = CameraData("Camera 1", "192.168.0.1");
    camera2 = CameraData("Camera 2", "192.168.0.2");
    camerasData = CamerasData()
    camerasData.add(camera1)
    camerasData.add(camera2)

    camerasData.save("cameras.test.data");

    camerasDataLoad = CamerasData.load("cameras.test.data");
    count = camerasDataLoad.getCount()
    camera1Name = camerasDataLoad.get(0).name
    camera2Name = camerasDataLoad.get(1).name

    if (count != 2 or camera1Name != "Camera 1" or camera2Name != "Camera 2"):
        print("count", count, "camera1Name", camera1Name, "camera2Name", camera2Name)
        raise Exception("Cameras data is incorrect");
    
    print("all testing passed")

if __name__ == "__main__":
    test()

