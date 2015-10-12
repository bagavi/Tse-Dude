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
    ContextLengthMax = 10





Obj = SimpleDude.System( ContextLengthMin = ContextLengthMin, ContextLengthMax = ContextLengthMax, flipProbab=flipProbab, shouldIprint = False)
Obj.mainRealData('../original/genome.fasta', 'Results_real.csv')
print( "total execution time", time.time() - StartTime)
