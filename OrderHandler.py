from Order import Order, ORDER_PAID_STATUS, ORDER_TESTPENDING_STATUS
import Labratory
from LabPriceCalculator import LabPriceCalculator
import database as db
from PaymentHandler import PaymentHandler

class OrderHandler:
    def __init__(self, patient):
        self.__tempTestList = []
        self.__patient = patient
        self.__laboratoryList = [] # (lab, price)
        self.__selectedLabId = None
    
    def hasInsurance(self):
        return not (self.__patient == None)

    def makeNewOrder(self):
        self.__order = Order(self.__patient)
        return Order.prepareTestData(self.__patient.getPrescription())

    def __setTestItems(self, testsId):
        self.__order.createTestItems(testsId)

    def __prepareLabPriceData(self):
        data = []
        for lp in self.__laboratoryList:
            data.append(({
                "id" : lp[0].getId(),
                "name" : lp[0].getName(),
                "priceRate" : lp[0].getPriceRate()
            }, lp[1]))
        return data


    def getLaboratoriesAndPrices(self, testsId):
        self.__setTestItems(testsId)
        lapPriceCalculator = LabPriceCalculator(self.__patient, testsId, self.__order)
        self.__laboratoryList = lapPriceCalculator.calculateLabPrice()

        return self.__prepareLabPriceData()

    def selectLaboratory(self, labId):
        self.__selectedLabId = labId
        for lab in self.__laboratoryList:
            if lab[0].getId() == labId:
                self.__order.setPrice(lab[1])
                return lab[1]

    def handlePayment(self):
        paymentResult = PaymentHandler().callPaymentApi()
        if paymentResult:
            self.__order.setStatus(ORDER_PAID_STATUS)
        return paymentResult

    def showTimes(self):
        for lab in db.db.labratories:
            if lab.getId() == self.__selectedLabId:
                times = lab.findClosestTimeSlots(self.__order)
                return lab.prepareTimeSlots(times)
    
    def selectTimeSlot(self, timeSlot):
        for lab in db.db.labratories:
            if lab.getId() == self.__selectedLabId:
                lab.reserveTesterAndTimeSlot(timeSlot)
                self.__order.setTime(Labratory.Labratory.findTimeSlotById(timeSlot))
                self.__order.setStatus(ORDER_TESTPENDING_STATUS)
                db.db.orders.append(self.__order)
        return self.__showResult()

    def __showResult(self):
        content = {
            'name:': self.__patient.getName(),
            'last name:': self.__patient.getLastName(),
            'order status:': self.__order.getStatus(),
            'time:': self.__order.getTime().createHashTime(),
            'price:': self.__order.getPrice()
        }
        return content