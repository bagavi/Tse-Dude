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
    flipProbab = 0.1

if len( sys.argv )> 3:
    ContextLengthMin = int( sys.argv[3] )
else:
    ContextLengthMin = 1


if len( sys.argv )> 4:
    ContextLengthMax = int( sys.argv[4] )
else:
    ContextLengthMax = 6
    

if len( sys.argv )> 5:
    ReadLength = int( sys.argv[5] )
else:
    ReadLength = 200
    

    
filename = '../original/genome_data.fasta'
ReadLength = 100


shouldIprint =  lambda x, y: False

Obj = SimpleDude.System( ContextLengthMin = ContextLengthMin, ContextLengthMax = ContextLengthMax, flipProbab=flipProbab, shouldIprint=shouldIprint)
Obj.ReadSimulation( filename, ReadLength = ReadLength )
print( "total execution time", time.time() - StartTime)