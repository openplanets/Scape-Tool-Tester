import os
from scapetesting.govdocs1.govdocs1 import loadTruths, cache

__author__ = 'abr'

outFile = 'scapetesting/govdocs1/csv/complete.csv'
print os.path.abspath(outFile)

loadTruths()

fileThing = open(outFile, mode="w")

for key,truth in cache.groundTruths.items():
        print >> fileThing, truth

fileThing.close()
        

#truthCounters = {}

#for key,truth in cache.groundTruths.items():
#    key = str(truth.baseMime)
#    counter = truthCounters.get(key,0)
#    counter +=1
#    truthCounters[key] = counter

#for key,counter in sorted(truthCounters.items()):
#    print key+":"+str(counter)


