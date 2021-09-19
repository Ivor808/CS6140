from glob import glob
import matplotlib.pylab as plt
import os
import math
import decimal

## file paths
hamPath = 'HamSpam/ham/'
hamFiles = glob( hamPath + '*.words')
spamPath = 'HamSpam/spam/'
spamFiles = glob(spamPath + '*.words')
testPath = 'HamSpam/test/'
testFiles = glob(testPath + '*.words')


## Hyperparamaters

alpha = 0.001

## Vocab total
vocab = 8000

## spam and ham counts
hamWords = dict()
hamWordsCount = 0
hamEmailCount = 0

spamWords = dict()
spamWordsCount = 0
spamEmailCount = 0
## Calculate ham words total and counts of each
for file in hamFiles:
    f = open(file, "r")
    read = f.readlines()
    hamEmailCount += 1
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
    spamEmailCount += 1
    for word in read:
        word = word.strip()

        if word in spamWords:
            spamWords[word] += 1
        else:
            spamWords[word] = 1
            spamWordsCount +=1

h_total = 0
p_total = 0
## smoothing - remember to take the log of each
for val in hamWords:
    hamWords[val] = hamWords[val] + alpha / (hamWordsCount + (alpha * vocab))
    hamWords[val] = math.log(hamWords[val])
    h_total += hamWords[val]
    

for val in spamWords:
    spamWords[val] = spamWords[val] + alpha / (spamWordsCount + (alpha * vocab))
    spamWords[val] = math.log(spamWords[val])
    p_total += spamWords[val]

spamProb = spamEmailCount / (spamEmailCount + hamEmailCount)
hamProb = hamEmailCount / (spamEmailCount + hamEmailCount)


## test model?
## issues with normalization/
## id on test file doesnt work
count = 1
for file in testFiles:
    f = open(file, 'r')
    read = f.readlines()
    pspam  = spamProb
    pham = hamProb
    for word in read:
        word = word.strip()
        if word in hamWords:
            pham *= hamWords[word]
        if word in spamWords:
            pspam *= spamWords[word]
    if pspam > pham:
        print(str(count) + ":spam")
    else:
        print(str(count) + ":ham")
    count += 1


        


