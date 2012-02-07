import os
import time

import subprocess
from scapetesting.toolevaluation.toolEvaluation import ToolEvaluation

from scapetesting.toolevaluation.util import ensure_dir
from scapetesting.govdocs1 import govdocs1


__author__ = 'abr'



print("running")


def fileRunner(datafile, reportfile):
    with open(datafile,mode="rb") as dataFilePointer:
        with open(ensure_dir(reportfile),mode="w") as reportFilePointer:
            start = time.time()
            subprocess.check_call(["file","-i","-"],stdin=dataFilePointer,stdout=reportFilePointer)
            end = time.time()
            return end-start
    return

def fileParser(reportFile,datafile):
    #print ("opening ", reportFile)
    type = ""
    encoding = ""
    with open(reportFile) as f:
        for line in f:
            if line.startswith('/dev/stdin: '):
                type = line[len('/dev/stdin: '):].strip()
                type = type.split(";")[0]
    os.remove(reportFile)
    return [type]

fileEval = ToolEvaluation()
fileEval.verbal = False
fileEval.groundTruth = govdocs1.groundTruth
fileEval.tool = fileRunner
fileEval.reportParser = fileParser
