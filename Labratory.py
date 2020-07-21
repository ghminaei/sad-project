MORNING = 'Morning'
NOON = 'Noon'

import TimeSlotClass
import database as db

class Labratory:
    def __init__(self, lid):
        self.__id = lid
        self.__testers = []
        self.__resultTemplate = ""
        self.__availableTests = []
    
    def setTesters(self, testers):
        self.__testers = testers
    
    def setName(self, name):
        self.__name = name
    
    def getName(self):
        return self.__name
    
    def setPriceRate(self, rate):
        self.__priceRate = rate
    
    def getPriceRate(self):
        return self.__priceRate
            
    def getId(self):
        return self.__id
    
    def prepareTimeSlots(self, testerAndTimes):
        data = []
        for key, val in testerAndTimes.items():
            for t in val:
                data.append({
                    "id" : t.getId(),
                    "hash" : t.createHashTime()
                })
        return data
    
    @staticmethod
    def findTimeSlotById(timeId):
        for ts in db.db.timeSlots:
            if ts.getId() == timeId:
                return ts
            
    def findClosestTimeSlots(self, order):
        testerAndTimes = {}
        suitableTimes = self.__extractSuitableTimes(order)
        if len(suitableTimes):
            allMorning, allNoon = self.__determineTimeRange(suitableTimes)
            if (allMorning) or (not allMorning and not allNoon):
                testerAndTimes = self.__findMorningAvailableTime()
            elif allNoon:
                testerAndTimes = self.__findNoonAvailableTime()
        else:
            testerAndTimes = self.__findAvailableTimeWithoutLimit()
        return testerAndTimes
    
    def checkOrderAvailability(self, order):
        testerAndTimes = {}
        testerAndTimes = self.findClosestTimeSlots(order)
        deletedKeys = []
        for key in testerAndTimes.keys():
            if len(testerAndTimes[key]) == 0:
                deletedKeys.append(key)
        for dk in deletedKeys:
            del testerAndTimes[dk]
        return bool(testerAndTimes)

    def __extractSuitableTimes(self, order):
        suitableTimes = []
        for test in order.getTestItems():
            if test.getTestPreCondition()['suitableTime']:
                suitableTimes.append(test.getTestPreCondition()['suitableTime'])
        return suitableTimes
    def __determineTimeRange(self, suitableTimes):
        allMorning = True
        allNoon = True
        for time in suitableTimes:
            if time == MORNING:
                allNoon = False
            elif time == NOON:
                allMorning = False
        return allMorning, allNoon
    def __findMorningAvailableTime(self):
        testerAndTimes = {}
        availbaleTimesHash = []
        for tester in self.__testers:
            testerAndTimes[tester.getId()] = []
            for time in tester.getAvailableTimes():
                if time.getStart() < 10:
                    if time.createHashTime() not in availbaleTimesHash:
                        testerAndTimes[tester.getId()].append(time)
                        availbaleTimesHash.append(time.createHashTime())
                        if len(availbaleTimesHash) == 3:
                            return testerAndTimes
        return testerAndTimes
    def __findNoonAvailableTime(self):
        testerAndTimes = {}
        availbaleTimesHash = []
        for tester in self.__testers:
            testerAndTimes[tester.getId()] = []
            for time in tester.getAvailableTimes():
                if time.getStart() > 10:
                    if time.getHash() not in availbaleTimesHash:
                        testerAndTimes[tester.getId()].append(time)
                        availbaleTimesHash.append(time.getHash())
                        if len(availbaleTimesHash) == 3:
                            return testerAndTimes
        return testerAndTimes
    def __findAvailableTimeWithoutLimit(self):
        testerAndTimes = {}
        availbaleTimesHash = []
        for tester in self.__testers:
            testerAndTimes[tester.getId()] = []
            for time in tester.getAvailableTimes():
                if time.getHash() not in availbaleTimesHash:
                    testerAndTimes[tester.getId()].append(time)
                    availbaleTimesHash.append(time.getHash())
                    if len(availbaleTimesHash) == 3:
                        return testerAndTimes
        return testerAndTimes
    def reserveTesterAndTimeSlot(self, time): #is this necessary?
        for tester in self.__testers:
            for availableTime in tester.getAvailableTimes():
                if availableTime.getId() == time:
                    tester.reserveTimeSlot(time)
                    break
    def setAvailableTests(self, availableTests):
        self.__availableTests = availableTests
    def getAvailableTests(self):
        return self.__availableTests