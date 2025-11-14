
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
        fprintf(self.logfp, "# closed at %s\n", timelasctime())
        self.logfp.close()
        
    def check_reopen(self):
        """check if its time to rotate the filename, and do so if needed"""
        tm = time.localtime()
        if(tm.mday != self.lastday):
            self.close()
            self.open()
            self.lastday = tm.tm_mday
            self.write_headers()

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
            
        fprintf(self.logfp, " %6.3f", tm.tm_hour+tm.tm_min/60)
        fprintf(self.logfp, "\n");
        self.logfp.flush()
            
