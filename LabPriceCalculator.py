import database as db
from ExceptionHandler import NoLabratoryFound
from InsuranceHandler import InsuranceHandler
from Order import Order

class LabPriceCalculator:
    def __init__(self, patient, testList, order):
        self.__patient = patient
        self.__testList = testList
        self.__order = order

    def calculateLabPrice(self):
        labList = self.__getLabList()
        return self.__calculatePrices(labList)
    
    def __getLabList(self):
        labList = []
        for lab in db.db.labratories:
            existence = True
            for test in self.__testList:
                if test not in lab.getAvailableTests():
                    existence = False
                    break
            if existence and lab.checkOrderAvailability(self.__order):
                labList.append(lab)
        if len(labList) == 0:
            raise NoLabratoryFound()
        return labList
    
    def __calculatePrices(self, labList): #patient knows insurance
        patientInsurance = self.__patient.getInsurance()
        hasInsurance = InsuranceHandler().verifyInsurance(patientInsurance.getInsuranceId())
        labAndPrice = []
        for lab in labList:
            labPrice = 0
            for testId in self.__testList:
                test = Order.findTestById(testId)
                labPrice += (test.getBasePrice()) * lab.getPriceRate()
            if patientInsurance and hasInsurance:
                discount = labPrice * patientInsurance.getInsuranceRate()
                if discount <= patientInsurance.getInsuranceCeiling():
                    labPrice -= discount
                else:
                    labPrice -= patientInsurance.getInsuranceCeiling()
            labAndPrice.append((lab, labPrice))
        return labAndPrice
    