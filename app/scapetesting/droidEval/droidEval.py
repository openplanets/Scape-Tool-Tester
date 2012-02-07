import csv
import os
import subprocess
import tempfile
import time
import sys
from scapetesting.govdocs1 import govdocs1
from scapetesting.toolevaluation.toolEvaluation import ToolEvaluation
from scapetesting.toolevaluation.util import ensure_dir

__author__ = 'abr'


print("running")


_groundTruth = govdocs1.groundTruth

identificationsKeyToMime = {}

#First, we run droid on the entire stuff in datadir
_droidPath = "/home/abr/Downloads/droid/droid.sh"

def droidRunner(reportfile):
    dataDir = govdocs1.dataDir
    with open(ensure_dir(reportfile),mode="w") as reportFilePointer:
        start = time.time()
        subprocess.call(["bash",_droidPath,"-a",dataDir,"-R","-p",reportfile],cwd=os.path.dirname(_droidPath), stderr=sys.stdout)
        end = time.time()
    return end-start

#Then we droid-parse the report file

#then we csv parse the report file
def droidReportParser(reportfile):
    tempdir = tempfile.mkdtemp()
    csvReportfile = os.path.join(tempdir,"report.csv")
    try:
        start = time.time()
        subprocess.call(["bash",_droidPath,"-p",reportfile,"-q","-e",csvReportfile],cwd=os.path.dirname(_droidPath),stderr=sys.stdout)
        end = time.time()
        fileThing = open(csvReportfile, mode="rt")
        reader = csv.DictReader(f=fileThing, fieldnames=["ID","PARENT_ID","URI","FILE_PATH","NAME","METHOD","STATUS","SIZE","TYPE","EXT","LAST_MODIFIED","EXTENSION_MISMATCH","MD5_HASH","FORMAT_COUNT","PUID","MIME_TYPE","FORMAT_NAME","FORMAT_VERSION"], delimiter=",")

        for line in reader:
            filename = line["NAME"]
            mime = line["MIME_TYPE"]
            type = line["TYPE"]
            if type == 'Folder':
                continue
            filename = filename.split(".")[0]
            try:
                key = int(filename)
            except ValueError:
                continue
            existingMimes = identificationsKeyToMime.get(key,[])
            existingMimes.append(mime)
            identificationsKeyToMime[key] = existingMimes
        fileThing.close()
    finally:
        os.remove(csvReportfile)
        os.rmdir(tempdir)





#The parser operation just retrieve the entry from the parsed csv file

def droidParser(unusedReportFile,datafile):
    #print ("opening ", reportFile)
    filename = datafile.split(".")[0]
    key = int(filename)
    mime = identificationsKeyToMime.get(key,[])
    return mime


droidEval = ToolEvaluation()

droidEval.groundTruth = _groundTruth
droidEval.reportParser = droidParser
droidEval.verbal = True


#the Runner operation is noop
def noop(x,y): return 0
droidEval.tool = noop
