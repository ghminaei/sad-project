from ExceptionHandler import *
COL = ": "
LOGIN_CMD = "login"
USERNAME_MSG = "username"
PASSWORD_MSG = "password"
NEWORDER_CMD = "neworder"
LABPRICES_MSG = "lalaboratory and prices"
CHOOSE_TESTS_CMD = "choosetest"
SELECT_LAB_CMD = "selectlab"
PAYMENT_CMD = "payment"
SELECT_TIMESLOT_CMD = "selecttimeslot"
EXIT_CMD = "exit"

ALL_CMD = [
    LOGIN_CMD,
    NEWORDER_CMD,
    CHOOSE_TESTS_CMD,
    SELECT_LAB_CMD,
    PAYMENT_CMD,
    SELECT_TIMESLOT_CMD,
    EXIT_CMD
]


USER_INIT_STATUS = "INIT"
USER_LOGGED_STATUS = "LOGGED"
USER_NEWORDER_STATUS = "NEWORDER"
USER_TEST_CHOSEN_STATUS = "TESTCHOSEN"
USER_LAB_SELECTED_STATUS = "LABSELECTED"
USER_PAID_STATUS = "PAID"
USER_TIME_SELECTED_STATUS = "TIMESELECTED"

from OrderHandler import *
from Patient import *

def loginHandler():
    while True:
        username = input("username: ")
        password = input("password: ")
        patient = None
        try:
            patient = Patient.login(username, password)
            userStatus = USER_LOGGED_STATUS
            print("logged in successfully")
            return userStatus, patient
        except UsernamaNotFound:
            print("Username not found!")
            print("Please try again:")
        except PasswordNotValid:
            print("Username or Password is incorrect!")
            print("Please try again:")

def showTests(testList):
    print("Tests are:")
    for tl in testList:
        print("number: {}, suitable time: {}, patient prepare: {}, description: {}, base price: {}".format(tl["id"], tl["preCondition"]["suitableTime"], tl["preCondition"]["patientPrepare"], tl["description"], tl["basePrice"]))

def newOrderHandler(patient):
    orderHandler = OrderHandler(patient)
    testList = orderHandler.makeNewOrder()
    showTests(testList)
    return USER_NEWORDER_STATUS, orderHandler

def showLabPrices(labPriceList):
    print("List of Labs")
    for lp in labPriceList:
        print("number: {}, name: {}, price rate: {} -- price: {}".format(lp[0]["id"], lp[0]["name"], lp[0]["priceRate"], lp[1]))

def chooseTestsHandler(orderHandler):
    testIDs = [int(i) for i in input("enter test item numbers e.g. 1 2 3: ").split()]
    try:
        labPriceList = orderHandler.getLaboratoriesAndPrices(testIDs)
        if not orderHandler.hasInsurance():
            print("Warning! you don't have a valid insurance")
        showLabPrices(labPriceList)
        return USER_TEST_CHOSEN_STATUS
    except NoLabratoryFound:
        print("You should do tests in different labs and orders")
        return USER_LOGGED_STATUS
    

def showFinalPrice(priceLab):
    print("final price: ")
    print(priceLab)

def selectLabHandler(orderHandler):
    labId = int(input("enter lab number: "))
    priceLab = orderHandler.selectLaboratory(labId)
    showFinalPrice(priceLab)
    return USER_LAB_SELECTED_STATUS


def showTimeSlots(timeSlotList):
    print("Time slots: ")
    for t in timeSlotList:
        print("id: {}, time: {}".format(t["id"], t["hash"]))

def paymentHandler(orderHandler):
    if orderHandler.handlePayment():
        timeSlotList = orderHandler.showTimes()
        print("Payment successfully!")
        showTimeSlots(timeSlotList)
        return USER_PAID_STATUS
    else:
        print("please try again")

def showResult(result):
    print("Result:")
    print("name: {} {}".format(result["name:"], result["last name:"]))
    print("Order status:", result["order status:"])
    print("Time:", result["time:"])

def selectTimeSlotHandler(orderHandler):
    timeSlotId = int(input("enter time slot number: "))
    result = orderHandler.selectTimeSlot(timeSlotId)
    showResult(result)
    return USER_TIME_SELECTED_STATUS

def validateInput(cmd, userStatus):
    if cmd == LOGIN_CMD and userStatus == USER_INIT_STATUS:
        return 
    elif cmd == NEWORDER_CMD and userStatus == USER_LOGGED_STATUS:
        return
    elif cmd == CHOOSE_TESTS_CMD and userStatus == USER_NEWORDER_STATUS:
        return
    elif cmd == SELECT_LAB_CMD and userStatus == USER_TEST_CHOSEN_STATUS:
        return
    elif cmd == PAYMENT_CMD and userStatus == USER_LAB_SELECTED_STATUS:
        return
    elif cmd == SELECT_TIMESLOT_CMD and userStatus == USER_PAID_STATUS:
        return
    elif cmd == EXIT_CMD:
        return
    else:
        raise NotAValidCmd()

def commandHandler():
    patient = None
    orderHandler = None
    userStatus = USER_INIT_STATUS
    while True:
        cmd = input("command: ")
        try:
            validateInput(cmd, userStatus)
            if cmd == LOGIN_CMD:
                userStatus, patient = loginHandler()
            elif cmd == NEWORDER_CMD:
                userStatus, orderHandler = newOrderHandler(patient)
            elif cmd == CHOOSE_TESTS_CMD:
                userStatus = chooseTestsHandler(orderHandler)
            elif cmd == SELECT_LAB_CMD:
                userStatus = selectLabHandler(orderHandler)
            elif cmd == PAYMENT_CMD:
                userStatus = paymentHandler(orderHandler)
            elif cmd == SELECT_TIMESLOT_CMD:
                userStatus = selectTimeSlotHandler(orderHandler)
            elif cmd == EXIT_CMD:
                print("bye!")
                break
        except:
            print("not a valid cmd, try again")
