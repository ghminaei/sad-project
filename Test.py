from database import *

class Test:
    def __init__(self, tid):
        self.__id = tid
    def setTestDescription(self, description):
        self.__description = description
    def getId(self):
        return self.__id
    def getTestDescription(self):
        return self.__description
    def setTestPreCondition(self, preCondition):
        self.__preCondition = preCondition
    def getTestPreCondition(self):
        return self.__preCondition
    def setBasePrice(self, basePrice):
        self.__basePrice = basePrice
    def getBasePrice(self):
        return self.__basePrice