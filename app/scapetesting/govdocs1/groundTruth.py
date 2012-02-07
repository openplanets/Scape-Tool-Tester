__author__ = 'abr'


class FileTruth(object):
    accuracy = ""
    baseMime = []
    charset = ""
    digest = ""
    extensions = []
    fileName = ""
    id = ""
    kind = ""
    size = 0
    version = []

    def __str__(self):

        str_lst = [str(value) for prop,value in sorted(self.__dict__.items(),key = lambda prop: prop[0])]
        #str_lst = [self.fileName]
        return '\t'.join(str_lst) + "\n"



    def __init__(self, filename, size, type, notes, extensions, accuracy, metadata, kind, id, Y, digest, decoder, equivalentMimes):
        self.accuracy = accuracy
        self.baseMime = getMime(int(id),type, decoder, equivalentMimes)
        self.charset = getCharset(type)
        self.digest = digest
        self.extensions = extensions
        self.fileName = filename
        self.id = id
        self.kind = kind
        self.size = size
        self.version = getVersion(notes, metadata)






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

