import time, SimpleDude, CommonFunctions, sys
StartTime = time.time()
# From terminal


if len( sys.argv )> 1 :
    flipProbab = float( sys.argv[1] )
else:
    flipProbab = 0.05

if len( sys.argv )> 2:
    ContextLengthMin = int( sys.argv[2] )
else:
    ContextLengthMin = 3


if len( sys.argv )> 3:
    ContextLengthMax = int( sys.argv[3] )
else:
    ContextLengthMax = 6




shouldIprint =  lambda x, y: False

Obj = SimpleDude.System( ContextLengthMin = ContextLengthMin, ContextLengthMax = ContextLengthMax , MarkovSequenceLength=0, flipProbab=flipProbab, shouldIprint=shouldIprint)
Obj.DependenceonLength()
print( "total execution time", time.time() - StartTime)
