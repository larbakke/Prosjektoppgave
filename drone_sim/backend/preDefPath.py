from typing import List
from position import Position


class PreDefPath:
    def  __init__(self, path: List[Position] = None):
        if path == None:
            self.path = []
        else:
            self.path = path
        self.next = None
        if len(self.path) > 0:
            self.next = path[0]
        self.complete = False
        self.completedSteps = []
        self.currentStep = 0

    def addPath(self, path: List[Position]):
        if len(self.path) == 0:
            self.path = path
            self.next = path[0]
        else:
            self.path.extend(path)

        if self.next == None:
            self.next = path[0]

    def getNext(self) -> Position:
        return self.next
    
    def completeStep(self):
        self.completedSteps.append(self.path[self.currentStep])
        self.currentStep += 1
        if self.currentStep == len(self.path):
            self.complete = True
            self.next = None
        else:
            self.next = self.path[self.currentStep]

    def isComplete(self) -> bool:
        return self.complete
    
    def addStep(self, step: Position):
        self.path.append(step)
        
    def overRidePath(self, path):
        self.path = path
        self.next = path[0]
        self.complete = False
        self.currentStep = 0

    def getCompletedSteps(self) -> List[Position]:
        return self.completedSteps
    


