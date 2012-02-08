__author__ = 'abr'


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


