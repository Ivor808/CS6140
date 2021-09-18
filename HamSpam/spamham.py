## for each email we iterate and save each word in respective dictionary spot. Do this on both sets
## count words and email totals
from glob import glob

import os

## file paths
hamPath = 'HamSpam/ham/'
hamFiles = glob( hamPath + '*.words')
spamPath = 'HamSpam/spam/'
spamFiles = glob(spamPath + '*.words')


## Hyperparamaters

alpha = 0.005

## spam and ham counts
hamWords = dict()
hamWordsCount = 0

spamWords = dict()
spamWordsCount = 0

## Calculate ham words total and counts of each
for file in hamFiles:
    f = open(file, "r")
    read = f.readlines()
    for word in read:
        word = word.strip()

        if word in hamWords:
            hamWords[word] += 1
        else:
            hamWords[word] = 1
            hamWordsCount +=1

for file in spamFiles:
    f = open(file, "r")
    read = f.readlines()
    for word in read:
        word = word.strip()

        if word in spamWords:
            spamWords[word] += 1
        else:
            spamWords[word] = 1
            spamWordsCount +=1

print(spamWordsCount)