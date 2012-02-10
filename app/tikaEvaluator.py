import os
import subprocess
import tempfile
import sys
import time
from scapetesting.fidoEval import fidoParser
from scapetesting.fidoEval.fidoParser import fidoReportLoader
from scapetesting.tikaEval import TikaParser
from scapetesting.tikaEval.TikaParser import tikaReportLoader

__author__ = 'abr'

_tikaWrapperPath = "/home/abr/Projects/git/TikaWrapper/target/tikaWrapper-0.0.2-SNAPSHOT-jar-with-dependencies.jar"

def tikaRunner(csvReportFile):
    dataDir = '/home/abr/Downloads/000/'
    with open(csvReportFile,"w") as fileThing:
        start = time.time()
        subprocess.call(["java", "-jar",_tikaWrapperPath,dataDir],cwd=os.path.dirname(_tikaWrapperPath), stdout=fileThing,stderr=fileThing)
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

