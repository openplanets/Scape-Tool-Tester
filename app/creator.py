import os
from scapetesting.govdocs1.govdocs1 import loadTruths, cache

__author__ = 'abr'

outFile = 'scapetesting/govdocs1/csv/complete.csv'
print os.path.abspath(outFile)

loadTruths()
fileThing = open(outFile, mode="w")

for key,truth in cache.groundTruths.items():
    fileThing.write(str(truth))
fileThing.close()
