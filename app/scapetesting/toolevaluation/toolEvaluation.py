#!/usr/bin/python
import csv
import os
import tempfile
import sys
from scapetesting.toolevaluation.util import ensure_dir
from scapetesting.govdocs1 import govdocs1


class ToolEvaluation(object):

    reportParser = NotImplemented
    groundTruth = govdocs1.groundTruth
    verbal = True
    tool = NotImplemented
    problems = {}
    timing = {}

    def _compareTypes(self,identifiedTypes, truth):

        result = []
        try:
            for type in truth.baseMime:
                if identifiedTypes is None or identifiedTypes == []:
                    return result
                for identifyType in identifiedTypes:

                    if str(identifyType).strip().startswith(str(type).strip()):
                        result.append(identifyType)
            return result
        except TypeError:
            return []



    def analyseTool(self, datadir=govdocs1.dataDir, reportdir=None):
        global filesNumber, errorNumber
        filesNumber = 0
        errorNumber = 0
        self.problems.clear()
        if reportdir is None:
            reportdir = tempfile.mkdtemp()
        try:
            self._recursion(datadir,reportdir,lambda a,b,c,d: self._analyseAndCheck(a,b,c,d))
        finally:
            print "Logs from the running is in "+reportdir
            print "Files scanned "+str(filesNumber)
            print "Files in error "+str(errorNumber)
            for truth,identified in sorted(self.problems.items()):
                total = 0
                for error,number in sorted(identified.items()):
                    if  not error == "Correct":
                        total += number

                total += identified.get("Correct",0)
                print "" + truth + ":" + str(identified.get("Correct",0))+ ":"+str(total)
                for error,number in sorted(identified.items()):
                    if  not error == "Correct":
                        print "\t"+error + "\t:\t" + str(number)
        for millis in sorted(self.timing.keys()):
            print str(self.timing[millis]) + " files were identified in "+str(millis)+"ms"





    def _analyseAndCheck(self, datadir,reportdir,root,file):

        global filesNumber, errorNumber
        filepath = os.path.join(datadir,root,file)

        truth = self.groundTruth(filepath)
        if truth is None: #There is no groundTruth for this file, ignore
            return
        if not truth.baseMime:
            return
        reportFilePath = ensure_dir(os.path.join(reportdir,root,file+".output.log"))

        time = self.tool(filepath,reportFilePath)
        millis = round(time*1000,0)
        self.timing[millis] = self.timing.get(millis,0)+1

        identifiedTypes = sorted(self.reportParser(reportFilePath,file))
        identifiedTypesKey = ", ".join(identifiedTypes)
        if identifiedTypesKey == "":
            identifiedTypesKey = "None"
        filesNumber+=1
        key = ", ".join(truth.baseMime)
        overlapOfTypes = self._compareTypes(identifiedTypes,truth)
        if self.verbal:
            print filepath+":"+identifiedTypesKey
        if overlapOfTypes == []:
            errorNumber+=1
            try:
                previousProblems = self.problems[key]
            except KeyError:
                previousProblems = {}
            try:
                wrongHits = previousProblems[identifiedTypesKey]
            except KeyError:
                wrongHits = 0
            wrongHits +=1
            previousProblems[identifiedTypesKey] = wrongHits
            self.problems[key] = previousProblems
            if self.verbal:
                print "GroundTruth marks it as", truth.baseMime
                print
        else:
            identifiedType = "Correct"
            try:
                previousProblems = self.problems[key]
            except KeyError:
                previousProblems = {}
            try:
                rightHits = previousProblems[identifiedType]
            except KeyError:
                rightHits = 0
            rightHits +=1
            previousProblems[identifiedType] = rightHits
            self.problems[key] = previousProblems







    def _recursion(self,datadir, reportdir, operation):
        for root, dirs, files in os.walk(datadir):
            if files:
                for file in sorted(files):
                    operation(datadir,reportdir,root,file)

