from datetime import datetime, time, timedelta
import urllib.request
from astral import Astral, Location
from pytz import timezone

class ScheduledObject():
    def __init__(self, name, ip, urlOn, urlOff, id):
        self.id = id
        self.name = name
        self.ip = ip
        self.urlOn = urlOn
        self.urlOff = urlOff
        self.on_times = []
        self.status = "off"

    def add_on_time(self, startTime, endTime):
        self.on_times.append((startTime, endTime))

    def _get_url(self, url):
        urllib.request.urlopen(url)

    def turn_on(self):
        self._get_url("http://" + self.ip + "/" + self.urlOn)

    def turn_off(self):
        self._get_url("http://" + self.ip + "/" + self.urlOff)

    def toggle(self):
        if self.status == "off":
            self.status = "on"
            self.turn_on()
        else:
            self.status = "off"
            self.turn_off()

    def init(self):
        self.turn_off()

    def localize_time(t):
        d = datetime.today()
        return ScheduledObject.localize_date(datetime.combine(d, t))

    def localize_date(d):
        stockholm = timezone('Europe/Stockholm')
        return stockholm.localize(d)

    def update(self):
        print("Updating {}".format(self.name))
        localized_now = ScheduledObject.localize_date(datetime.now())

        previousStatus = self.status
        self.status = "off"

        for (a, b) in self.on_times:
            a_date = ScheduledObject.localize_time(a)
            b_date = ScheduledObject.localize_time(b)

            if a_date <= localized_now <= b_date:
                self.status = "on"
        
        if previousStatus == "off" and self.status == "on":
            print("Turning lamp on!")
            self.turn_on()
        elif previousStatus == "on" and self.status == "off":
            print("Turning lamp off!")
            self.turn_off()


