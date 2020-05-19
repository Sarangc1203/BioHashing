from IrisRecognitionCasia.code.scan_procedure.iris_scan import IrisScan
import os
import tlsh
import random
import matplotlib.pyplot as plt
from time import sleep

curr_dir = os.path.dirname(os.path.realpath(__file__))
srand1 = 'abcdefghijklmnopqrstuvwxyz'
srand2 = ''.join(random.sample(srand1,26))      # RANDOM STRING TO BE APPENDED TO THE IRISCODES DURING HASHING

irisCodeDataset = []    # USED FOR HASHING (STRING FORMAT)
allDataset = []         # FOR PRINTING ALL IRISCODES (INTEGER FORMAT)

for subject in os.listdir(curr_dir+"/dataset/"):
    for subfold in os.listdir(curr_dir+"/dataset/"+subject):
        allcodes = []
        for img in os.listdir(curr_dir+"/dataset/"+subject+"/"+subfold):
            iriscode = IrisScan.scan_iris(curr_dir+"/dataset/"+subject+"/"+subfold+"/"+img)
            # print("dataset/"+subject+"/"+subfold+"/"+img+":\n"+iriscode+"\n\n")
            strind = 0      # START INDEX FOR HORIZONTAL SHIFTING
            for c in range(len(iriscode)):
                if iriscode[c] != '0':
                    strind = c
                    break
            # print(strind)
            iriscode_new = iriscode[strind:strind+5000]     # LENGTH OF IRISCODE DEFINED TO BE 5000 AS OF NOW
            allcodes.append(iriscode_new)
            acc = []
            for c in iriscode_new:
                acc.append(int(c))
            allDataset.append(acc)
        irisCodeDataset.append(allcodes)

crosshashing = []
for x1 in irisCodeDataset:
    for y1 in x1:
        tempstr1 = srand2+y1
        hex1 = tlsh.hash(str.encode(tempstr1))
        acc = []
        for x2 in irisCodeDataset:
            for y2 in x2:
                tempstr2 = srand2+y2
                hex2 = tlsh.hash(str.encode(tempstr2))
                acc.append(tlsh.diff(hex1,hex2))
        crosshashing.append(acc)

plt.ion()
plt.imshow(allDataset, cmap='gray', interpolation='none', aspect='auto')
plt.show(block=True)
plt.imshow(crosshashing, cmap='gray', interpolation='none')
plt.show(block=True)
