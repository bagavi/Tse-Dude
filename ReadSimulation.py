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
    ContextLengthMin = 7


if len( sys.argv )> 3:
    ContextLengthMax = int( sys.argv[3] )
else:
    ContextLengthMax = 10
    
if len( sys.argv )> 4:
    alphamin = int( sys.argv[4] )
else:
    alphamin = 1
    
if len( sys.argv )> 5:
    alphamax = int( sys.argv[5] )
else:
    alphamax = 10
    

if len( sys.argv )> 6:
    ReadLength = int( sys.argv[6] )
else:
    ReadLength = 100
    

    
filename = '../original/genome_data.fasta'


shouldIprint =  lambda x, y: False

Obj = SimpleDude.System( ContextLengthMin = ContextLengthMin, ContextLengthMax = ContextLengthMax, flipProbab=flipProbab, shouldIprint=shouldIprint, alphamin = alphamin, alphamax = alphamax)
Obj.ReadSimulation( filename, ReadLength = ReadLength )
print( "total execution time", time.time() - StartTime)
