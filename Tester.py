from database import *
from User import *
from TimeSlotClass import TIMESLOT_AVAILABLE_STATUS, TIMESLOT_UNAVAILABLE_STATUS

class Tester(User):
    def __init__(self, tid):
        User.__init__(self, tid)
        self.__allTimes = []

    def getAvailableTimes(self):
        allAvailabelTimes = []
        for t in self.__allTimes:
            if t.getStatus() == TIMESLOT_AVAILABLE_STATUS:
                allAvailabelTimes.append(t)
        return allAvailabelTimes
    
    def setAllTimes(self, allTimes):
        self.__allTimes = allTimes

    def reserveTimeSlot(self, timeId):
        for t in self.__allTimes:
            if timeId == t.getId():
                t.setStatus(TIMESLOT_UNAVAILABLE_STATUS)
