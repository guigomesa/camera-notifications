import time

class TimerProcess:
    def __init__(self, intervalInSeconds):
        self.intervalInSeconds = intervalInSeconds
        self.startTime = time.time()
        self.data = []
    
    def isOpened(self):
        seconds = time.time() - self.startTime
        return seconds <= self.intervalInSeconds
    
    def isClosed(self):
        return not self.isOpened()

    def addData(self, data):
        self.data.append(data)

    def getData(self):
        return self.data
