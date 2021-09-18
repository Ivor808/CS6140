## for each email we iterate and save each word in respective dictionary spot. Do this on both sets
## count words and email totals
from glob import glob

import os
hamPath = '/ham/'
files = glob( hamPath + '*.words');

##f = open('ham/1.words')
##print(f.readline())
print(os.getcwd())


for file in files:
    f = open(file, "r")
    print(f.readline())

