import csv, Bio, os
from Bio import SeqIO, Seq

handle = open('..\original\\genome_data.fasta')

CombinedSeq = ""
for seq_record in SeqIO.parse( handle, "fasta") :
    CombinedSeq = seq_record 
a = 10
handle.close()
