import csv
import os
from scapetesting import govdocs1
from scapetesting.govdocs1 import groundTruth
from scapetesting.toolevaluation.reportParser import ToolPrecisionTest


__author__ = 'abr'



print("running")


_groundTruth = groundTruth.groundTruths

identificationsKeyToMime = {}


def fileReportLoader(reportFile):
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

def fileParser(filename):
    #print ("opening ", reportFile)
    filename = os.path.basename(filename)
    filename = filename.split(".")[0]
    key = int(filename)
    mime = identificationsKeyToMime[key]
    return mime


fileEval = ToolPrecisionTest()
fileEval.verbal = True
fileEval.groundTruth = govdocs1.groundTruth

fileEval.reportParser = fileParser
