import os
import subprocess
import time
from config import dataDir


__author__ = 'abr'

def md5sumRunner(reportfile):
    with open(reportfile,"w") as fileThing:
        start = time.time()
        for dir, dirs, files in os.walk(dataDir):
            if files:
                for file in sorted(files):
                    startLocal = time.time()
                    print file
                    subprocess.check_call(["md5sum",os.path.join(dir,file)],stdout=fileThing)
                    endLocal = time.time()
        end = time.time()
    return end-start





csvReportfile = "md5sumreport.csv"
print csvReportfile
try:
    time = md5sumRunner(csvReportfile)
    pass
finally:
    pass

print "Time spent analysing the entire archive: "+str(time)+" seconds"




