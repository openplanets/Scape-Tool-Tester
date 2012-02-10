import os
import subprocess
import tempfile
import time
import config
from scapetesting.tikaEval import TikaParser
from scapetesting.tikaEval.TikaParser import tikaReportLoader

__author__ = 'abr'



def tikaRunner(csvReportFile):

    with open(csvReportFile,"w") as fileThing:
        start = time.time()
        subprocess.call(["java", "-jar",config._tikaWrapperPath, config.dataDir],cwd=os.path.dirname(config._tikaWrapperPath), stdout=fileThing,stderr=fileThing)
        end = time.time()
        return end-start

tempdir = tempfile.mkdtemp()
csvReportfile = os.path.join(tempdir,"report.csv")
print csvReportfile
try:
    time = tikaRunner(csvReportfile)
    tikaReportLoader(csvReportfile)
finally:
    pass
    os.remove(csvReportfile)
    os.rmdir(tempdir)

print "Time spent analysing the entire archive: "+str(time)+" seconds"
TikaParser.tikaEval.analyseTool()

