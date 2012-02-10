import os
import subprocess
import tempfile
import sys
import time
from config import dataDir
import config
from scapetesting.fidoEval import fidoParser
from scapetesting.fidoEval.fidoParser import fidoReportLoader

__author__ = 'abr'



def fidoRunner(csvReportFile):

    with  open(csvReportFile,"w") as    fileThing:
        start = time.time()
        subprocess.call(
            ["python2.6",config._fidoPath,"-recurse",dataDir],
            cwd=os.path.dirname(config._fidoPath),
            stdout=fileThing,
            stderr=fileThing)
        end = time.time()
        return end-start

tempdir = tempfile.mkdtemp()

csvReportfile = os.path.join(tempdir,"report.csv")
print csvReportfile
try:
    time = fidoRunner(csvReportfile)
    fidoReportLoader(csvReportfile)
finally:
    pass
    os.remove(csvReportfile)
    os.rmdir(tempdir)

print "Time spent analysing the entire archive: "+str(time)+" seconds"
fidoParser.fidoEval.analyseTool()

