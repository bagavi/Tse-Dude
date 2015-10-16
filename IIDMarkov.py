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
    ContextLength = int( sys.argv[3] )
else:
    ContextLength = 1




Ratio = .7
markovTransitionProbab = .8
shouldIprint =  lambda x, y: False

Obj = SimpleDude.System(  ContextLength = ContextLength , MarkovSequenceLength=SequenceLength, flipProbab=flipProbab, shouldIprint=shouldIprint)
Obj.IIDMarkov(markovTransitionProbab)
I = Obj.Input.Sequence
C = Obj.Output.ReceivedSequence
O = Obj.Output.Sequence
# 
# for i in range(len(I)):
#     if ( I[i] != O[i] ):
#         print( i )
#         print( "In", I[i-3:i+4])
#         print( "Re", C[i-3:i+4])
#         print( "Ou", O[i-3:i+4], "\n")
#         a= 10
print( "total execution time", time.time() - StartTime)
