from ScheduledObject import ScheduledObject
import sys

sys.path.insert(0, './pyHS100')
from pyHS100 import SmartBulb, SmartPlug

class ScheduledTplink(ScheduledObject):
    def __init__(self, name, ip, tpType):
        self.name = name
        self.ip = ip
        self.urlOn = ""
        self.urlOff = ""
        self.on_times = []
        self.status = "off"
        self.override = False
        if tpType == "bulb":
            self.tpObj = SmartBulb(ip)
        elif tpType == "plug":
            self.tpObj = SmartPlug(ip)
        else:
            self.tpObj = None

    def turn_on(self):
        print(" - Turning on!")
        self.status = "on"
        self.tpObj.turn_on()

    def turn_off(self):
        print(" - Turning off!")
        self.status = "off"
        self.tpObj.turn_off()

