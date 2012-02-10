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
def droidReportLoader(csvReportfile):

    with open(csvReportfile, mode="rt") as fileThing:
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







#The parser operation just retrieve the entry from the parsed csv file

def droidParser(datafile):
    #print ("opening ", reportFile)
    filename = datafile.split(".")[0]
    key = int(filename)
    mime = identificationsKeyToMime[key]
    return mime


droidEval = ToolPrecisionTest()

droidEval.reportParser = droidParser
droidEval.verbal = True

