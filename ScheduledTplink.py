from ScheduledObject import ScheduledObject
import sys

sys.path.insert(0, './pyHS100')
from pyHS100 import SmartBulb, SmartPlug

class ScheduledTplink(ScheduledObject):
    def __init__(self, name, ip, tpType, isDimmable=False):
        ScheduledObject.__init__(self, name, ip, "", "", isDimmable)  

        if tpType == "bulb":
            self.tpObj = SmartBulb(ip)
        elif tpType == "plug":
            self.tpObj = SmartPlug(ip)
        else:
            self.tpObj = None

    def turn_on(self):
        print(" - Turning on!")
        self.status = "on"
        try:
           self.tpObj.turn_on()
        except:
           print("Cannot access tplink {}".format(self.ip))
            
        

    def turn_off(self):
        print(" - Turning off!")
        self.status = "off"
        try:
           self.tpObj.turn_off()
        except:
           print("Cannot access tplink {}".format(self.ip))

    def set_brightness(self, brightness):
        if self.isDimmable:
            try:
                self.tpObj.brightness = brightness
            except:
                print("Cannot access tplink {}".format(self.ip))

    def get_brightness():
        if self.isDimmable:
            return self.tpObj.brightness
        else:
            return 100
