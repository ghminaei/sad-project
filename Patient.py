import database as db
from User import *
from ExceptionHandler import *
# from main import db as db

class Patient(User):
    def __init__(self, pid):
        User.__init__(self, pid)
        self.wantNewOrder = False
        self.__insurance = None
    def setAge(self, age):
        self.__age = age
    def getAge():
        return self.__age
    def setDisease(self, disease):
        self.__disease = disease
    def getDisease(self):
        return self.__disease
    def setInsurance(self, insurance):
        self.__insurance = insurance
    def getInsurance(self):
        return self.__insurance
    def setPrescription(self, prescription):
        self.__prescription = prescription
    def getPrescription(self):
        return self.__prescription
    @staticmethod
    def login(username, password):
        foundPatient = False
        for patient in db.db.patients:
            if patient.validateUsername(username):
                foundPatient = True
                if patient.validatePassword(password):
                    return patient
                else:
                    raise PasswordNotValid()
        if not foundPatient:
            raise UsernameNotFound()
    def __newOrder():
        #mitunim masalan ye flag true konim
        self.wantNewOrder = True