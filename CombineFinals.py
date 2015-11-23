import re, csv, os
from CommonFunctions import *

files = os.listdir()

Finalfiles = []

for i in files:
    if re.match("Final_*", i) != None:
        Finalfiles.append(i)

Allresults = [ [ "InputSequence Length", "Channel Flip Prob", "Context Length", "Markov Transition Probabilities","No. of Errors", "No of changes by DUDE", "Number of right changes", "fraction of changes", "fraction of right changes", "net Correction", "Coverage Depth", "Ratio", "Alpha", "DudeWin" ] ] 
for file in Finalfiles:
    Allresults += FiletoArray(file)

with open( "Finals.csv", 'w', newline='') as f:                                    
    writer = csv.writer(f)                                                       
    writer.writerows(Allresults)
f.close()