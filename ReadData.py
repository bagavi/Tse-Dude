import time, SimpleDude, CommonFunctions, sys
StartTime = time.time()
# From terminal

if len( sys.argv )> 1 :
    flipProbab = float( sys.argv[1] )
else:
    flipProbab = 0.1

if len( sys.argv )> 2:
    ContextLengthMin = int( sys.argv[2] )
else:
    ContextLengthMin = 3

if len( sys.argv )> 3:
    ContextLengthMax = int( sys.argv[3] )
else:
    ContextLengthMax = 7

if len( sys.argv )> 4:
    NoOfReads = int( sys.argv[4] )
else:
    NoOfReads = 500

shouldIprint =  lambda x, y: not( x in y )
shouldIprint =  lambda x, y: False
Obj = SimpleDude.System( ContextLengthMin = ContextLengthMin, ContextLengthMax = ContextLengthMax, flipProbab=flipProbab, shouldIprint = shouldIprint)
Obj.ReadData('../original/frag.fastq', NoOfReads,'Results_reads.csv')
print( "total execution time", time.time() - StartTime)

