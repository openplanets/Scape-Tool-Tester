__author__ = 'abr'

import csv
import os
import subprocess
import tempfile
import sys
from scapetesting.govdocs1 import groundTruth
from scapetesting.toolevaluation.reportParser import ToolPrecisionTest

__author__ = 'abr'


print("running")


_groundTruth = groundTruth.groundTruths

identificationsKeyToMime = {}


#then we csv parse the report file
def fidoReportLoader(csvReportfile):

    with open(csvReportfile, mode="rt") as fileThing:
        reader = csv.DictReader(f=fileThing, fieldnames=["OK","PARENT_ID","URI","DESCRIPTION","FORMAT_NAME","SIZE","NAME","MIME","METHOD"], delimiter=",")

        for line in reader:
            filename = line["NAME"]
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

def fidoParser(datafile):
    #print ("opening ", reportFile)
    filename = datafile.split(".")[0]
    key = int(filename)
    mime = identificationsKeyToMime[key]
    return mime


fidoEval = ToolPrecisionTest()

fidoEval.reportParser = fidoParser
fidoEval.verbal = True

