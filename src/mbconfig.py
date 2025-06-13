#!/usr/bin/python
#
# configuration classes and data store for 'monbox' tools
#

import sys
import time
sys.path.append('/home/tell/proj/python');
from perlish import *

class mbsensor:
    """class to hold all of the configuration info for a sensor measurement"""
    def __init__(self, fullname, dtype, ftag, mtype, mtopic):
        self.fullname = fullname # full descriptive name
        self.dtype = dtype	# data type string
        self.ftag = ftag  # forwarding tag / short name
        self.mtype = mtype	# mqtt type for conversion to floating point
        self.topic = mtopic	# mqtt topic
        self.last = None  # may get used to hold value
        self.lasttime = 0

    def __str__(self):
        return sprintf("<mbsensor full=\"%s\" dtype=%s ftag=%s", self.fullname, self.dtype, self.ftag);
    def __repr__(self):
        return sprintf("<mbsensor full=\"%s\" dtype=%s ftag=%s", self.fullname, self.dtype, self.ftag);

    def fstr_if_not_old(self, threshold):
        now = time.time()
        if(now - self.lasttime < threshold):
            return sprintf("&%s=%s", self.ftag, str(self.last))
        else:
            printf(" fstr_if %s too old now=%d lasttime=%d delta=%d\n", self.ftag, now, self.lasttime, now - self.lasttime)
            return ""
    
class mbslist:
    """class to hold list of mbsensor objects, with helper methods"""
    def __init__(self):
        self.mblist = []
        self.bytopic = None

    def print(self):
        pprint.pprint(self.mblist)

    def add(self, mbs):
        self.mblist.append(mbs)

    def init_static(self):
        """initialize with static or test data"""
        #                  fullname,                 datatype, ftag,       mqtt_type, mqtt_topic
        self.add( mbsensor("CPU Load",               "float",  "cpu_load", float,      "monbox/cpu_load") );
        self.add( mbsensor("CPU Temp",               "temp_c", "cpu_temp", float,      "monbox/cpu_temp") );
        self.add( mbsensor("Indoor LR Temp",         "temp_c", "indoor",   float,      "monbox/room_temp") );
        self.add( mbsensor("Indoor LR Humidity",     "rh",     "indoor_humid",  float, "monbox/room_humidity") );
        self.add( mbsensor("Outdoor/East 1820 Temp", "temp_c", "outdoor",  "18b20_json", "tele/tasmota_88E4AB/SENSOR") );
        self.add( mbsensor("Indoor Bedroom Temp",    "temp_c", "indoor3",  "18b20_json", "tele/tasmota_F99C40/SENSOR"));

        self.add( mbsensor("Outdoor Radio Temp",     "temp_c", "outdoor2", float,   "rtl_433/fullcircle/devices/Thermopro-TX2C/2/250/temperature_C"));
        self.add( mbsensor("LR Countertop Temp",     "temp_c", "indoor2", float,       "rtl_433/fullcircle/devices/Thermopro-TX2C/1/238/temperature_C"));

    def setup_data(self):
        """set up quick-access dictionaries.  call this after init_static or other sensor config load"""
        self.bytopic = dict()
        self.bytag = dict()
        for s in self.mblist:
            self.bytopic[ s.topic ] = s
            self.bytag[ s.ftag ] = s

if __name__ == "__main__":
    import sys
    import pprint
    mbl = mbslist()
    mbl.init_static()
    mbl.setup_data()
    mbl.print()
    pprint.pprint(mbl.__dict__)
    
    
    

