from glob import glob
import os
import math
import decimal
import re

## file paths
hamPath = "HamSpam/ham/"
hamFiles = glob(hamPath + "*.words")
spamPath = "HamSpam/spam/"
spamFiles = glob(spamPath + "*.words")
testPath = "HamSpam/test/"
testFiles = glob(testPath + "*.words")
truthPath = "HamSpam/"
truthName = "truthfile"
truthFile = truthPath + truthName


## Hyperparamaters
alpha = 0.01
vocab = 1000000

## spam and ham counts
hamWords = dict()
hamWordsCount = 0
hamEmailCount = 0

spamWords = dict()
spamWordsCount = 0
spamEmailCount = 0

## Calculate ham words total and counts of each
for file in hamFiles:
    with open(file, "r") as f:
        read = f.readlines()
        hamEmailCount += 1
        for word in read:
            word = word.strip("\n").lower()
            hamWordsCount += 1
            if word in hamWords:
                hamWords[word] += 1
            else:
                hamWords[word] = 1

for file in spamFiles:
    with open(file, "r") as f:
        read = f.readlines()
        spamEmailCount += 1
        for word in read:
            word = word.strip("\n").lower()
            spamWordsCount += 1
            if word in spamWords:
                spamWords[word] += 1
            else:
                spamWords[word] = 1


## Probability in log space
totalEmails = hamEmailCount + spamEmailCount
hamProb = hamEmailCount / totalEmails
spamProb = spamEmailCount / totalEmails
hamProb = math.log2(hamProb)
spamProb = math.log2(spamProb)

## Convert each count to a probability, then smooth it and put in log space

for word in hamWords:
    hamWords[word] = (hamWords[word] + alpha) / (hamWordsCount + alpha * vocab)
    hamWords[word] = math.log2(hamWords[word])

for word in spamWords:
    spamWords[word] = (spamWords[word] + alpha) / (spamWordsCount + alpha * vocab)
    spamWords[word] = math.log2(spamWords[word])

## Test our model
total = 0
truth_Table = []

## Load the truth labels
with open(truthFile, "r") as f:
    read = f.readlines()

    for word in read:
        word.strip("\n")
        val = int(word)
        truth_Table.append(val)
## Label the test emails via our model and add to confusion matrix
confusion_matrix = {"TP": 0, "FP": 0, "FN": 0, "TN": 0}
for file in testFiles:
    total += 1
    with open(file, "r") as f:

        count = int(re.match("^(\d+)", os.path.basename(f.name)).group())

        read = f.readlines()
        pspam = spamProb
        pham = hamProb
        for word in read:
            word = word.strip("\n").lower()
            if word in hamWords:
                pham += hamWords[word]
            else:
                pham += math.log2((alpha / (hamWordsCount + (alpha * vocab))))
            if word in spamWords:
                pspam += spamWords[word]
            else:
                pspam += math.log2((alpha / (spamWordsCount + (alpha * vocab))))

        ## Uncomment the prints to see each emails classification
        if pham >= pspam:
            ##print(str(count) + ":ham")
            if count in truth_Table:
                confusion_matrix["FN"] += 1
            else:
                confusion_matrix["TN"] += 1
        else:
            ##print(str(count) + ":spam")
            if count in truth_Table:
                confusion_matrix["TP"] += 1
            else:
                confusion_matrix["FP"] += 1


## Print the confusion matrix, precision, recall, and f1
print(confusion_matrix)
precision = confusion_matrix["TP"] / (confusion_matrix["TP"] + confusion_matrix["FP"])
recall = confusion_matrix["TP"] / (confusion_matrix["TP"] + confusion_matrix["FN"])
f1 = (2 * precision * recall) / (precision + recall)
print("Precision: " + str(precision))
print("Recall: " + str(recall))
print("f1: " + str(f1))
