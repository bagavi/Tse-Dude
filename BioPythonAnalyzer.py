import csv, Bio, os
from Bio import SeqIO, Seq

handle = open('..\original\\frag.fastq')

CombinedSeq = []
i = 0
good = 0
for seq_record in SeqIO.parse( handle, "fastq") :
    if( i  == 1000 ):
        break
    print (i)
    i += 1
    if 'N' not in list( seq_record.seq ):
        good += 1
        
    CombinedSeq += list(seq_record.seq)
print( good )
a = 10
handle.close()
