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

    def __index__(self):
        pass




