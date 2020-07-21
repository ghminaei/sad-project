from database import *

class Insurance:
    def __init__(self, insuranceId):
        self.__insuranceId = insuranceId
    
    def setType(self, insuranceType):
        self.__insuranceType = insuranceType 
    
    def setInsuranceCeiling(self, ceil):
        self.__insuranceCeiling = ceil

    def getInsuranceCeiling(self):
        return self.__insuranceCeiling
    
    def setInsuranceRate(self, insuranceRate):
        self.__insuranceRate = insuranceRate

    def getInsuranceRate(self):
        return self.__insuranceRate

    def getInsuranceId(self):
        return self.__insuranceId
