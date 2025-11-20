
import time
from perlish import *

class ssv_logfile:
    """class to help handle space-separated value logfile"""
    def __init__(self, basename, dataheaders):
        self.basename = basename
        self.dataheaders = dataheaders

    def open(self):
        tm = time.localtime()
        timestr = time.strftime("%y%m%d", tm)
        self.lastday = tm.tm_mday
        logfname = sprintf("%s.%s", self.basename, timestr);
        #new_logfile = not(file_exists(logfname))
        self.logfp = open(logfname, "a");

    def close(self):
        """close a file"""
        fprintf(self.logfp, "# closed at %s\n", time.asctime())
        self.logfp.close()
        
    def check_reopen(self):
        """check if its time to rotate the filename, and do so if needed"""
        tm = time.localtime()
        if(tm.tm_mday != self.lastday):
            self.close()
            self.open()
            self.write_header()

    def write_header(self):
        """write headers for all of the columns.  including special hack first,last for our ha data convention"""
        fprintf(self.logfp, "#Time");
        for c in self.dataheaders:
            fprintf(self.logfp, " %s", c);
        fprintf(self.logfp, " floathour")
        fprintf(self.logfp, "\n")

    def write_data(self, datafields):
        """write a line of data"""
        tm = time.localtime()
        
        fprintf(self.logfp, "%02d:%02d", tm.tm_hour, tm.tm_min)
        for d in datafields:
            fprintf(self.logfp, " %s", d)
            
        fprintf(self.logfp, " %7.4f", tm.tm_hour+tm.tm_min/60)
        fprintf(self.logfp, "\n");
        self.logfp.flush()
            
if __name__ == "__main__":
    import sys
    import pprint
    import argparse

    parser =  argparse.ArgumentParser(description="monbox-config and data store test/demo");
    parser.add_argument("--verbose", "-v", default=False, action='store_true');
    parser.add_argument("--test", "-t", default=False, action='store_true');

    logbasename="mylogtest"
    
    headers = ["time", "value"]
    
    mylog = ssv_logfile(logbasename, headers)
    mylog.open()
    mylog.write_header()
    logfields = [0, 1];     mylog.write_data(logfields)
    logfields = [1, 2];     mylog.write_data(logfields)
    mylog.check_reopen()
    mylog.close()
    
