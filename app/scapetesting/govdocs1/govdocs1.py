import csv
import os
from scapetesting.govdocs1.groundTruth import FileTruth


__author__ = 'abr'

#dataDir = '/home/abr/.gvfs/sftp for scape on iapetus/home/scape/working/tooltest/005/'
dataDir = '/home/abr/Downloads/000/'
truthFile = '/home/abr/Downloads/govdocsDetails 6-25-2010.csv'


thisDir = os.path.abspath(os.path.dirname(__file__))
dicFile = thisDir+'/csv/mimetype-decoder.csv'
equivFile = thisDir+'/csv/mimetype-equiv.csv'


class Cache(object):
    groundTruths = {}
    _decoder = {}
    _equivMimes = {}
    decodingDone = False
    _loadingDone = False
    equivMimesDone = False

    @property
    def loadingDone(self):
        return self._loadingDone

    @loadingDone.setter
    def loadingDone(self, value):
        self._loadingDone = value

    def insert(self, index, value):
        self.groundTruths[int(index)] = value


    def insertDecoding(self, id, mime):
        self._decoder[int(id)] = mime


    def getTruth(self, index):
        try:
            return self.groundTruths[int(index)]
        except ValueError:
            return None

    def decode(self, id):
        return self._decoder[int(id)]

    def equivMimes(self, mime):
        return self._equivMimes[mime]

    def insertEquivMime(self, mime, mimes):
        mime = mime.strip()
        mimes = [mimetemp.strip() for mimetemp in mimes]
        existing = self._equivMimes.get(mime,[])
        self._equivMimes[mime] = existing + mimes


cache = Cache()



def loadDictionary():
    loadEquivMimes()
    if cache.decodingDone:
        return
    print "Loading decoder dictionary"
    fileThing = open(dicFile, mode="rt")
    reader = csv.DictReader(fileThing, fieldnames=["mime", "type", "extensions", "something", "other", "date", "id"],
        restkey="rest", delimiter=",")
    for line in reader:
        id = int(line["id"])
        mime = line["mime"]
        cache.insertDecoding(id, mime)

    cache.decodingDone = True
    fileThing.close()
    print "Decoder Dictionary loaded"

def loadTruths():
    loadDictionary()
    if cache.loadingDone:
        return
    print "Loading ground truths"
    fileThing = open(truthFile, mode="rt")
    reader = csv.DictReader(fileThing, fieldnames=["filename", "size", "type", "notes", "extensions", "accuracy", "metadata", "kind", "id", "Y", "digest"],
        restkey="rest", delimiter=";")
    for line in reader:

        filename = line["filename"]
        if filename == 'Filename+Ext':
            continue
        filename = filename.split(".")[0]
        truth = FileTruth()
        truth.fileName = filename
        for key,value in line.items():

            if truth.__dict__.has_key(key):
                truth.__dict__[key] = value
        truth.baseMime = getMime(int(truth.id),line["type"], cache.decode, cache.equivMimes)
        truth.version = getVersion(line["notes"], line["metadata"])
        if not truth.baseMime == []:
            cache.insert(filename,truth)
    cache.loadingDone = True
    fileThing.close()
    print "Ground truths loaded"




problems = {}

def getMime(id, type, decoder, equivalentMimes):
    try:
        mime = decoder(id)
        try:
            mimes = equivalentMimes(mime)
        except KeyError:
            mimes = []
        return [mime] + mimes
    except KeyError:
        problems[id] = type
        return []


def getCharset(line):
    None

def getVersion(notes, metadata):
    formatIndex = notes.find("Format v")
    version = []
    if formatIndex >= 0:
        start = formatIndex+len("Format v")
        end =  start+4
        temp = notes[start:end]
        version.append(temp)
    splits = metadata.split("; ")
    for split in splits:
        if split.startswith("File Version: "):
            version.append(split[len("File Version: "):])
    return version





def groundTruth(filepath):
    if not cache.loadingDone:
        loadComplete()
    try:
        filename = os.path.basename(filepath)
        filename = filename.split(".")[0]
        myTruth = cache.getTruth(filename)
        return myTruth
    except KeyError:
        return None


def loadEquivMimes():
    if cache.equivMimesDone:
        return
    print "Loading equivalent mimes"
    try:
        fileThing = open(equivFile, mode="rt")
    except IOError:
        print "Could not read "+os.path.abspath(equivFile)
        raise IOError
    reader = csv.DictReader(fileThing, fieldnames=["mime", "mimes"],
        restkey="rest"
        , delimiter="=")
    for line in reader:
        mime = line["mime"].strip();
        mimesStr = line["mimes"]
        if mimesStr is None:
            continue
        mimes = mimesStr.split(",")
        mimes = map(lambda s: s.strip(),mimes)
        cache.insertEquivMime(mime,mimes)

    cache.equivMimesDone = True
    fileThing.close()
    print "Equivalent mimes loaded"
#    for (mime,mimes) in cache._equivMimes.items():
#        print mime
#        for mimeType in mimes:
#            print mimeType
#        print


