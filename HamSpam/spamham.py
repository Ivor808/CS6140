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

hAdded = 0
pAdded = 0;

for val in hamWords:
    hamWords[val] += 1
    hAdded += 1

for val in spamWords:
    spamWords[val] +=1
    pAdded +=1

spamProb = spamEmailCount / (spamEmailCount + hamEmailCount)
hamProb = hamEmailCount / (spamEmailCount + hamEmailCount)

## smoothing - remember to take the log of each
for val in hamWords:
    hamWords[val] =  (hamWords[val] / (hamWordsCount + hAdded))
    ##hamWords[val] = math.log(hamWords[val])
    h_total += hamWords[val]
    

for val in spamWords:
    spamWords[val] = spamWords[val] / (spamWordsCount + pAdded)
    ##spamWords[val] = math.log(spamWords[val])
    p_total += spamWords[val]

## P(H) * P(f1) * (Pf2)

## lets calculate scores to get an idea of how the model is doing

## test model?
## issues with normalization/
## id on test file doesnt work
count = 1
for file in testFiles:
    f = open(file, 'r')
    read = f.readlines()
    pspam  = 1
    pham = 1
    for word in read:
        word = word.strip()
        if word in hamWords:
            pham = hamWords[word] * pham
        else:
            pham *= (1/hamWordsCount + hAdded)
        if word in spamWords:
            pspam = spamWords[word] * pspam
        else:
            pspam *= (1/spamWordsCount + pAdded)
    pspam = pspam * spamProb
    pham = pham * hamProb

    if pspam > pham:
        print(str(count) + ":spam")
    else:
        print(str(count) + ":ham")
    count += 1


        


