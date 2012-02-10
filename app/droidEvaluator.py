import os
import subprocess
import tempfile
import sys
import time
import config
from scapetesting.droidEval import droidParser

from scapetesting.droidEval.droidParser import droidReportLoader
from scapetesting.toolevaluation.util import ensure_dir

__author__ = 'abr'



def droidRunner(reportfile,csvReportFile):

    with open(ensure_dir(reportfile),mode="w") as reportFilePointer:
        start = time.time()
        subprocess.call(["bash",config._droidPath,"-a", config.dataDir,"-R","-p",reportfile],cwd=os.path.dirname(
            config._droidPath), stderr=sys.stdout)
        end = time.time()
        subprocess.call(["bash",config._droidPath,"-p",reportfile,"-q","-e",csvReportfile],cwd=os.path.dirname(
            config._droidPath),stderr=sys.stdout)
    return end-start

tempdir = tempfile.mkdtemp()
reportFile = os.path.join(tempdir,"reportFile.bin")
csvReportfile = os.path.join(tempdir,"report.csv")
try:
    time = droidRunner(reportFile,csvReportfile)
    droidReportLoader(csvReportfile)
finally:
    os.remove(reportFile)
    os.remove(csvReportfile)
    os.rmdir(tempdir)

print "Time spent analysing the entire archive: "+str(time)+" seconds"
droidParser.droidEval.analyseTool()

