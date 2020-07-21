from database import *

class User:
    def __init__(self, uid):
        self.__id = uid
    def setUsername(self, username):
        self._username = username
    def getUsername(self):
        return self._username
    def setName(self, name):
        self._name = name
    def getName(self):
        return self._name
    def setLastName(self, lastName):
        self._lastName = lastName
    def getLastName(self):
        return self._lastName
    def setGender(self, gender):
        self._gender = gender
    def getGender(self):
        return self._gender
    def setPhoneNumber(self, phoneNumber):
        self._phoneNumber = phoneNumber
    def getPhoneNumber(self):
        return self._phoneNumber
    def setPassword(self, password):
        self._password = password
    def getId(self):
        return self.__id

    def validateUsername(self, username):
        if self._username == username:
            return True
        return False
    def validatePassword(self, password):
        if self._password == password:
            return True
        return False