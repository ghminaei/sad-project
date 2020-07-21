from database import *

TIMESLOT_AVAILABLE_STATUS = "Available"
TIMESLOT_UNAVAILABLE_STATUS = "Unavailable"
class TimeSlot:
    def __init__(self, year, month, day, start, end, tid, status):
        self.__id = tid
        self.__start = start
        self.__end = end
        self.__year = year
        self.__month = month
        self.__day = day
        self.__status = status
    def setStatus(self, status):
        self.__status = status
    def getStatus(self):
        return self.__status
    def getStart(self):
        return self.__start
    def getEnd(self):
        return self.__end
    def getDay(self):
        return self.__day
    def getId(self):
        return self.__id
    def createHashTime(self):
        hash = ''
        hash = hash + str(self.__year) + '/'
        hash = hash + str(self.__month) + '/'
        hash = hash + str(self.__day) + ':'
        hash = hash + str(self.__start) + '-'
        hash += str(self.__end)
        return hash