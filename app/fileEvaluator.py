import os
import subprocess
import tempfile
import time
from config import dataDir
from scapetesting.fileEval.FileEvaluation import fileReportLoader, fileEval

__author__ = 'abr'

def fileRunner(reportfile):
    with open(reportfile,"w") as fileThing:
        start = time.time()
        for dir, dirs, files in os.walk(dataDir):
            if files:
                for file in sorted(files):
                    startLocal = time.time()
                    subprocess.check_call(["file","-i",os.path.join(dir,file)],stdout=fileThing)
                    endLocal = time.time()
        end = time.time()
    return end-start



tempdir = tempfile.mkdtemp()

csvReportfile = os.path.join(tempdir,"report.csv")
print csvReportfile
try:
    time = fileRunner(csvReportfile)
    fileReportLoader(csvReportfile)
    pass
finally:
    pass
    os.remove(csvReportfile)
    os.rmdir(tempdir)

print "Time spent analysing the entire archive: "+str(time)+" seconds"
fileEval.analyseTool()



