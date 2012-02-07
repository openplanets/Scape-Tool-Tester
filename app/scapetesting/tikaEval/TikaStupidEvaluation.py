import time
import subprocess
from scapetesting.govdocs1 import govdocs1
from scapetesting.toolevaluation.toolEvaluation import ToolEvaluation
from scapetesting.toolevaluation.util import ensure_dir


__author__ = 'abr'



print("running")


_groundTruth = govdocs1.groundTruth

_tikaPath= '/home/abr/Tools/tika/tika-app-1.0.jar'
_verbal = True


def tikaRunner(datafile, reportfile):
    with open(datafile,mode="rb") as dataFilePointer:
        with open(ensure_dir(reportfile),mode="w") as reportFilePointer:
            start = time.time()
            subprocess.call(["java","-jar",_tikaPath,"-m","-"],stdin=dataFilePointer,stdout=reportFilePointer)
            end = time.time()
            return end-start
    return

def tikaParser(reportFile,datafile):
    #print ("opening ", reportFile)
    type = ""
    encoding = ""
    with open(reportFile) as f:
        for line in f:
            if line.startswith('Content-Type: '):
                type = line[len('Content-Type: '):].strip()
            if line.startswith('Content-Encoding: '):
                encoding = line[len('Content-Encoding: '):].strip()
    return type, encoding

tikaEval = ToolEvaluation()

tikaEval.groundTruth = _groundTruth
tikaEval.reportParser = tikaParser
tikaEval.verbal = _verbal
tikaEval.tool = tikaRunner


