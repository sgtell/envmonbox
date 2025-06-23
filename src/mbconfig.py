#!/usr/bin/python
#
# configuration classes and data store for 'monbox' tools
#

import sys
import time
import yaml

sys.path.append('/home/tell/proj/python');
from perlish import *

class mbsensor_base:
    """base class for mbsensor/mbgen/etc"""
    def __init__(self):
        self.mbtype = 'mbbase'
        self.last = None  # may get used to hold value
        self.lasttime = 0
        self.forward = False
        self.ftag = '';
        self.column = 0;

    @property
    def topic(self):
        return None

    def fstr_if_not_old(self, threshold):
        """string for forwarding to cgi server"""
        now = time.time()
        if(not self.forward):
            return ""
        if(now - self.lasttime < threshold):
            return sprintf("&%s=%s", self.ftag, str(self.last))
        else:
            printf(" fstr_if %s too old now=%d lasttime=%d delta=%d\n", self.ftag, now, self.lasttime, now - self.lasttime)
            return ""

class mbsensor(mbsensor_base):
    """class to hold all of the configuration info for a sensor measurement"""
    def __init__(self, fullname, rcolumn, forward, plot, dtype, ftag, mtype, mtopic):
        super().__init__()
        self.mbtype = 'mbsensor'
        self.fullname = fullname # full descriptive name
        self.dtype = dtype	# data type string
        self.ftag = ftag  # forwarding tag / short name
        self.mtype = mtype	# mqtt type for conversion to floating point
        self.mtopic = mtopic	# mqtt topic
        self.column = rcolumn    # relative column in datafile. not counting required time columns.  starting at 1.
        self.forward = forward  # forward True/False
        self.plot = plot	# plot True/False

    def __str__(self):
        return sprintf("<mbsensor full=\"%s\" dtype=%s ftag=%s", self.fullname, self.dtype, self.ftag);
    def __repr__(self):
        return sprintf("<mbsensor full=\"%s\" dtype=%s ftag=%s", self.fullname, self.dtype, self.ftag);

    @property
    def topic(self):
        return self.mtopic


class mbgen(mbsensor_base):
    """class to hold config info for generated/processed data items"""
    def __init__(self, fullname, rcolumn, forward, plot, dtype, ftag,  gfunc, gsource):
        super().__init__()
        self.mbtype = 'mbgen'
        self.fullname = fullname # full descriptive name
        self.column = rcolumn    # relative column in datafile. not counting required time columns.  starting at 1.
        self.forward = forward  # forward True/False
        self.plot = plot	# plot True/False
        self.dtype = dtype	# data type string
        self.ftag = ftag  # forwarding tag / short name
        self.gfunc = gfunc	# generating function name (string)
        self.gsource = gsource	# generating source

    def __str__(self):
        return sprintf("<mbgen full=\"%s\" dtype=%s ftag=%s", self.fullname, self.dtype, self.ftag);
    def __repr__(self):
        return sprintf("<mbgen full=\"%s\" dtype=%s ftag=%s", self.fullname, self.dtype, self.ftag);

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
        #                  fullname,                 rcol, fwd? plot? datatype, ftag,            mqtt_type, mqtt_topic
        self.add( mbsensor("CPU Load",               1,   True, False, "float",  "cpu_load",     float,      "monbox/cpu_load") );
        self.add( mbsensor("CPU Temp",               2,   True, False, "temp_c", "cpu_temp",     float,      "monbox/cpu_temp") );
        self.add( mbsensor("Indoor LR Temp",         3,   True, False, "temp_c", "room_temp",     float,      "monbox/room_temp") );
        self.add( mbsensor("Indoor LR Humidity",     4,   True, True,  "rh",     "room_humidity", float,      "monbox/room_humidity") );
        self.add( mbsensor("Outdoor/East 1820 Temp", 5,   True, False, "temp_c", "outdoor_temp",  "18b20_json", "tele/tasmota_88E4AB/SENSOR") );
        self.add( mbsensor("Indoor Bedroom Temp",    12,  True, False, "temp_c", "bedroom_indoor3", "18b20_json", "tele/tasmota_F99C40/SENSOR"));
        self.add( mbsensor("Outdoor Radio Temp",     8,   True, False, "temp_c", "outdoor_tx2_temp", float,   "rtl_433/fullcircle/devices/Thermopro-TX2C/2/250/temperature_C"));
        self.add( mbsensor("LR Countertop Temp",     10,  True, False, "temp_c", "indoor_tx2_temp",  float,   "rtl_433/fullcircle/devices/Thermopro-TX2C/1/238/temperature_C"));

        # not really sensors, but generated data somwhere in the pipeline
        self.add( mbgen("Indoor LR Temp",         6,   False, True, "temp_f", "room_temp_f",        "c_to_f", "room_temp"        ));  
        self.add( mbgen("Outdoor/East 1820 Temp", 7,   False, True, "temp_f", "outdoor_temp_f",     "c_to_f", "outdoor_temp"     ));  
        self.add( mbgen("Indoor Bedroom Temp",    13,  False, True, "temp_f", "bedroom_indoor3_f",  "c_to_f", "bedroom_indoor3"  ));  
        self.add( mbgen("Outdoor Radio Temp",     9,   False, True, "temp_f", "outdoor_tx2_temp_f", "c_to_f", "outdoor_tx2_temp" ));  
        self.add( mbgen("LR Countertop Temp",     11,  False, True, "temp_f", "indoor_tx2_temp_f",  "c_to_f", "indoor_tx2_temp"  ));  

    def setup_data(self):
        """set up quick-access dictionaries.  call this after init_static or other sensor config load"""
        self.bytopic = dict()
        self.bytag = dict()
        self.bycolumn = dict()  # would like array, but need to write by index, and python arrays don't expand
        self.maxcol = 0;
        for s in self.mblist:
            if(s.topic):
                self.bytopic[ s.topic ] = s
            self.bytag[ s.ftag ] = s
            self.bycolumn[ s.column ] = s;
            if(s.column > self.maxcol):
                self.maxcol = s.column
            # TODO check that column numbers are contiguous
            
    def set_value(self, ftag, value):
        if(ftag in self.bytag):
            self.bytag[ftag].last = value

    def col_head_list(self):
        r = list();
        for i in range(1, self.maxcol+1):
            r.append( self.bycolumn[i].ftag)
        return r;
            
if __name__ == "__main__":
    import sys
    import pprint
    import argparse

    parser =  argparse.ArgumentParser(description="monbox-config and data store test/demo");
    parser.add_argument("--verbose", "-v", default=False, action='store_true');
    parser.add_argument("--quiet", "-q", default=False, action='store_true');
    parser.add_argument("--yamlout", "-o", type=str, help="write config as yaml");
    args = parser.parse_args();
    
    mbl = mbslist()
    mbl.init_static()
    mbl.setup_data()
    if(args.verbose):
        mbl.print()
        pprint.pprint(mbl.__dict__)
    if(not args.quiet):
        for mbs in mbl.mblist:
            printf(" %20s %25s %12d %10s %6s\n", mbs.ftag, mbs.fullname, mbs.lasttime, str(mbs.last), mbs.plot)

    if(args.yamlout):
        with open(args.yamlout, "w") as f:
            yaml.dump(mbl.mblist, f);
    

