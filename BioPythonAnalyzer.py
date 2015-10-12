import csv, Bio, os
from Bio import SeqIO, Seq

handle = open('..\original\\frag.fastq')

CombinedSeq = Seq.Seq("")
for seq_record in SeqIO.parse( handle, "fastq") :
    CombinedSeq += seq_record
    if int(seq_record.id[10:-2])%1000 == 0:
        print ( seq_record.id )
    if int(seq_record.id[10:-2]) > 33000:
        break
Freq = dict()
for i in CombinedSeq:
    Freq[i] = Freq.get(i,0) + 1
a = 10
handle.close()
