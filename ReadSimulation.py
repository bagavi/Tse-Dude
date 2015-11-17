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
    ContextLengthMin = 2


if len( sys.argv )> 3:
    ContextLengthMax = int( sys.argv[3] )
else:
    ContextLengthMax = 7
    

if len( sys.argv )> 4:
    ReadLength = int( sys.argv[4] )
else:
    ReadLength = 100
    

    
filename = '../original/genome_data.fasta'


shouldIprint =  lambda x, y: False

Obj = SimpleDude.System( ContextLengthMin = ContextLengthMin, ContextLengthMax = ContextLengthMax, flipProbab=flipProbab, shouldIprint=shouldIprint)
Obj.ReadSimulation( filename, ReadLength = ReadLength )
print( "total execution time", time.time() - StartTime)
