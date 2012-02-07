
import os
import tempfile
import time
import sys
from scapetesting.fido import fido
from scapetesting.govdocs1 import govdocs1
from scapetesting.toolevaluation.toolEvaluation import ToolEvaluation


print sys.path



__author__ = 'abr'



class Args:
    pass
def print_matches(fullname, matches, delta_t, matchtype=''):
    self = fidoInst
    count = self.current_count
    group_size = len(matches)

    time = int(delta_t * 1000)
    filesize = self.current_filesize
    matchtype = matchtype
    global reportfile
    filekey = os.path.basename(fullname)
    filekey = os.path.splitext(filekey)[0]

    if len(matches) is 0:
        reportfile.write(", ".join([filekey,str(None)])+"\n")
    else:
        i = 0
        for (f, s) in matches:
            i += 1
            #group_index = i
            #puid = self.get_puid(f)
            #formatname = f.find('name').text
            #signaturename = s.find('name').text
            mime = f.find('mime')
            if mime is not None:
                mimetype = mime.text
            else:
                mimetype =  None
            version = f.find('version')
            version = version.text if version is not None else None


            reportfile.write(", ".join([filekey,str(mimetype)])+"\n")
    reportfile.flush()

def report_parser(unusedDir,datafile):
    global reportfile
    reportfile.seek(0)

    reportLines = reportfile.readlines()
    for report in reportLines:
        #print report
        splits = report.split(", ")

        reportfile.truncate(0)
        return map(lambda s: s.strip(), splits[1:])

    reportfile.truncate(0)
    return None


def tool(file,report):

    start = time.time()
    fidoInst.identify_file(file)
    end = time.time()
    return end-start

args = Args()
args.bufsize = None
args.q = False
args.matchprintf = None
args.nomatchprintf = None
args.zip = False
args.confdir = os.path.dirname(fido.__file__) + "/conf"

groundTruth = govdocs1.groundTruth

fidoInst = fido.Fido(quiet=args.q, bufsize=args.bufsize,
    printmatch=args.matchprintf, printnomatch=args.nomatchprintf, zip=args.zip, conf_dir=args.confdir, handle_matches=print_matches)



fidoToolEval = ToolEvaluation()
fidoToolEval.verbal = True
fidoToolEval.groundTruth = govdocs1.groundTruth

fidoToolEval.tool = tool
fidoToolEval.reportParser = report_parser


global reportfile
reportfile = tempfile.TemporaryFile()









