from scapetesting import govdocs1
from scapetesting.govdocs1 import groundTruth

__author__ = 'abr'



class ToolPrecisionTest(object):

    reportParser = NotImplemented
    groundTruth = govdocs1.groundTruth
    problems = {}
    verbal = True

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



    def analyseTool(self):
        global filesNumber, errorNumber
        filesNumber = 0
        errorNumber = 0
        self.problems.clear()
        groundTruth.loadComplete()
        for file in sorted(groundTruth.groundTruths.keys()):

            truth = groundTruth.groundTruths[file]
            try:
                identifiedTypes = sorted(self.reportParser(file))
            except KeyError:
                continue
            identifiedTypesKey = ", ".join(identifiedTypes)
            if identifiedTypesKey == "":
                identifiedTypesKey = "None"
            filesNumber+=1
            key = ", ".join(truth.baseMime)
            overlapOfTypes = self._compareTypes(identifiedTypes,truth)
            if self.verbal:
                print file+":"+identifiedTypesKey
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



