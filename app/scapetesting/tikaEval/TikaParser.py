import csv
import os
import time

import subprocess
from scapetesting import govdocs1
from scapetesting.toolevaluation.toolEvaluation import ToolEvaluation
from scapetesting.govdocs1 import groundTruth
from scapetesting.toolevaluation.reportParser import ToolPrecisionTest

from scapetesting.toolevaluation.util import ensure_dir


__author__ = 'abr'



print("running")


_groundTruth = groundTruth.groundTruths

identificationsKeyToMime = {}


def tikaReportLoader(reportFile):
    #print ("opening ", reportFile)
    type = ""
    encoding = ""
    with open(reportFile) as f:
        reader = csv.DictReader(f, fieldnames=["FILE","MIME"], delimiter=":")
        for line in reader:
            filename = line["FILE"]
            if filename is None or len(filename) == 0:
                continue
            mime = line["MIME"]
            filename = os.path.basename(filename)
            filename = filename.split(".")[0]
            try:
                key = int(filename)
            except ValueError:
                continue
            existingMimes = identificationsKeyToMime.get(key,[])
            existingMimes.append(mime)
            identificationsKeyToMime[key] = existingMimes



#The parser operation just retrieve the entry from the parsed csv file

def tikaParser(filename):
    #print ("opening ", reportFile)
    filename = os.path.basename(filename)
    filename = filename.split(".")[0]
    key = int(filename)
    mime = identificationsKeyToMime[key]
    return mime


tikaEval = ToolPrecisionTest()
tikaEval.verbal = True
tikaEval.groundTruth = govdocs1.groundTruth

tikaEval.reportParser = tikaParser
