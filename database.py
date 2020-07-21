import json
from Insurance import *
from Labratory import *
from Order import *
from Patient import *
from Tester import *
from TimeSlotClass import *
from Test import *

class database:
    def __init__(self, adr):
        self.patients = []
        self.orders = []
        self.tests = []
        self.insurances = []
        self.testers = []
        self.labratories = []
        json_file = open(adr)
        self.data = json.load(json_file)
        self.timeSlots = []
        self.run()
        

    def run(self):
        for i in self.data["Insurance"]:
            ins = Insurance(i["insuranceId"])
            ins.setType(i["type"])
            ins.setInsuranceCeiling(i["ceil"])
            ins.setInsuranceRate(i["rate"])
            self.insurances.append(ins)

        for i in self.data["Patient"]:
            p = Patient(i["id"])
            p.setName(i["name"])
            p.setUsername(i["username"])
            p.setLastName(i["family"])
            p.setGender(i["gender"])
            p.setPhoneNumber(i["phone"])
            p.setPassword(i["pass"])
            p.setAge(i["age"])
            p.setDisease(i["disease"])
            for ins in self.insurances:
                if ins.getInsuranceId() == i["insurance"]["insuranceId"]:
                    p.setInsurance(ins)
            p.setPrescription(i["prescription"])
            self.patients.append(p)

        for i in self.data["Test"]:
            t = Test(i["id"])
            t.setTestDescription(i["description"])
            t.setTestPreCondition(i["preCondition"])
            t.setBasePrice(i["basePrice"])
            self.tests.append(t)


        for i in self.data["TimeSlot"]:
            t = TimeSlot(i["year"], i["month"], i["day"], i["start"], i["end"], i["id"], i["status"])
            self.timeSlots.append(t)

        for i in self.data["Tester"]:
            t = Tester(i["id"])
            t.setName(i["name"])
            t.setLastName(i["family"])
            t.setGender(i["gender"])
            t.setPhoneNumber(i["phone"])
            allTimes = []
            for atid in i["available_time"]:
                for ts in self.timeSlots:
                    if atid == ts.getId():
                        allTimes.append(ts)
            t.setAllTimes(allTimes)
            self.testers.append(t)

        for i in self.data["Labratory"]:
            l = Labratory(i["id"])
            l.setName(i["name"])
            l.setAvailableTests(i["availableTests"])
            l.setPriceRate(i["priceRate"])
            allTesters = []
            for t in i["testers"]:
                for tester in self.testers:
                    if t == tester.getId():
                        allTesters.append(tester)
            l.setTesters(allTesters)
            self.labratories.append(l)
    
    def store(self, adr):
        json_file = open(adr, "r")
        self.NewData = json.load(json_file)
        self.NewData["Orders"] = []
        for o in self.orders:
            self.NewData["Orders"].append({
                "id": o.getId(),
                "status": o.getStatus(),
                "testItems": o.getTestItemsIds(),
                "patient": o.getPatient().getId(),
                "time": o.getTime().getId(),
                "price": o.getPrice()
                })
        
        for t in self.timeSlots:
            index = 0
            for tInData in self.NewData["TimeSlot"]:
                if t.getId() == tInData["id"] and t.getStatus() == TimeSlotClass.TIMESLOT_UNAVAILABLE_STATUS:
                    self.NewData["TimeSlot"][index]["status"] = TimeSlotClass.TIMESLOT_UNAVAILABLE_STATUS
                index += 1
        
        json_file = open(adr, "w")
        json.dump(self.NewData, json_file)



db = None