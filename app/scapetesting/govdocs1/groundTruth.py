import csv
import os

__author__ = 'abr'


groundTruths = {}
comleteFile = "/home/abr/Downloads/complete.csv"

class FileTruth(object):

    def __str__(self):

        str_lst = []
        for prop in sorted(self.__dict__.keys()):
            if not prop.startswith("__"):
                value = self.__dict__[prop]
                str_lst.append(str(value))
        return '\t'.join(str_lst) + "\n"

    def __init__(self):
        self.accuracy = ""
        self.baseMime = []
        self.charset = ""
        self.digest = ""
        self.extensions = []
        self.fileName = ""
        self.id = ""
        self.kind = ""
        self.size = 0
        self.version = []
        pass



def loadComplete():

    str_lst = [str(prop) for prop in sorted(FileTruth().__dict__.keys())]

    tmp_lst = str_lst[:]
    for prop in tmp_lst:
        if "__" in prop:
            str_lst.remove(prop)

    del tmp_lst

    try:
        fileThing = open(comleteFile, mode="rt")
    except IOError:
        print "Could not read "+os.path.abspath(comleteFile)
        raise IOError

    reader = csv.DictReader(fileThing, fieldnames=str_lst,
        restkey="rest"
        , delimiter="\t")
    for line in reader:
        truth = FileTruth()
        for prop,value in line.items():
            if value is not None and len(value) > 0 and value[0] is "[":
                value = value.replace("'","").replace("[","").replace("]","")
                values = value.split(",")
                values = map(lambda s: s.strip(),values)
                truth.__dict__[prop] = values
            else:
                truth.__dict__[prop] = value
        groundTruths[truth.fileName] = truth
    fileThing.close()
    pass
