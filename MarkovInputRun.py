import time, SimpleDude, CommonFunctions, sys
StartTime = time.time()
# From terminal

if len( sys.argv )> 1 :
    SequenceLength = int( float( sys.argv[1] ) )
else:
    SequenceLength = int( 1e3 )

if len( sys.argv )> 2 :
    flipProbab = float( sys.argv[2] )
else:
    flipProbab = 0.01

if len( sys.argv )> 3:
    ContextLengthMin = int( sys.argv[3] )
else:
    ContextLengthMin = 3


if len( sys.argv )> 4:
    ContextLengthMax = int( sys.argv[4] )
else:
    ContextLengthMax = 6





Obj = SimpleDude.System( ContextLengthMin = ContextLengthMin, ContextLengthMax = ContextLengthMax , MarkovSequenceLength=SequenceLength, flipProbab=flipProbab, shouldIprint=False)
Obj.Markov()
print( "total execution time", time.time() - StartTime)
