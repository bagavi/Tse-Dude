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
    ContextLengthMin = 5


if len( sys.argv )> 3:
    ContextLengthMax = int( sys.argv[3] )
else:
    ContextLengthMax = 10
    
if len( sys.argv )> 4:
    alphamin = int( sys.argv[4] )
else:
    alphamin = 0
    
if len( sys.argv )> 5:
    alphamax = int( sys.argv[5] )
else:
    alphamax = 30
    

if len( sys.argv )> 6:
    Repeat = int( sys.argv[6] )
else:
    Repeat = 20


if len( sys.argv )> 7:
    ReadLength = int( sys.argv[7] )
else:
    ReadLength = 100
    

    
filename = '../original/genome_data.fasta'


shouldIprint =  lambda x, y: False

Obj = SimpleDude.System( ContextLengthMin = ContextLengthMin, ContextLengthMax = ContextLengthMax, flipProbab=flipProbab, 
                         shouldIprint=shouldIprint, alphamin = alphamin, alphamax = alphamax, Repeat = Repeat)
Obj.ReadSimulation( filename, ReadLength = ReadLength )
print( "total execution time", time.time() - StartTime)
