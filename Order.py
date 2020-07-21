ORDER_DRAFT_STATUS = "Draft"
ORDER_PAID_STATUS = "Paid"
ORDER_TESTPENDING_STATUS = "TestPending"

import Test
import database as db


class Order:
    id = 0
    def __init__(self, patient):
        Order.id += 1
        self.__id = Order.id
        self.__status = ORDER_DRAFT_STATUS
        self.__testItem = []
        self.__patient = patient
        self.__time = None
        self.__price = None

    def getId(self):
        return self.__id
    def getTestItemsIds(self):
        return [i.getId() for i in self.__testItem]
    def setStatus(self, status):
        self.__status = status
    def getStatus(self):
        return self.__status
    def createTestItems(self, testItems):
        self.__testItem = Order.findTestsById(testItems)
    def getTestItems(self):
        return self.__testItem
    def setTime(self, time):
        self.__time = time
    def getTime(self):
        return self.__time
    def setPrice(self, price):
        self.__price = price
    def getPrice(self):
        return self.__price
    def getPatient(self):
        return self.__patient
    @staticmethod
    def findTestsById(testIds):
        foundTests = []
        for testId in testIds:
            for test in db.db.tests:
                if test.getId() == testId:
                    foundTests.append(test)
        return foundTests
    
    @staticmethod
    def findTestById(testId):
        test = Order.findTestsById([testId])
        return test[0]
    
    @staticmethod
    def prepareTestData(testIds):
        tests = Order.findTestsById(testIds)
        data = []
        for test in tests:
            data.append({
                "id" : test.getId(),
                "preCondition" : test.getTestPreCondition(),
                "description" : test.getTestDescription(),
                "basePrice" : test.getBasePrice()
            })
        return data

    