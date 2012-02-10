import os
import subprocess
import tempfile
import sys
import time
from scapetesting.fidoEval import fidoParser
from scapetesting.fidoEval.fidoParser import fidoReportLoader

__author__ = 'abr'

_fidoPath = "/home/abr/Downloads/openplanets-fido-991c16a/fido/fido.py"

def fidoRunner(csvReportFile):
    dataDir = '/home/abr/Downloads/000/'
    fileThing = open(csvReportFile,"w")
    start = time.time()
    subprocess.call(["python",_fidoPath,"-recurse",dataDir],cwd=os.path.dirname(_fidoPath), stdout=fileThing,stderr=fileThing)
    end = time.time()
    fileThing.close()
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

