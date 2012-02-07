import os
import tempfile
from scapetesting.droidEval.droidEval import droidRunner, droidReportParser, droidEval

__author__ = 'abr'


tempdir = tempfile.mkdtemp()
reportFile = os.path.join(tempdir,"reportFile.bin")
try:
    time = droidRunner(reportFile)
    droidReportParser(reportFile)
finally:
    os.remove(reportFile)
    os.rmdir(tempdir)

print "Time spent analysing the entire archive: "+str(time)+" seconds"
droidEval.analyseTool()
