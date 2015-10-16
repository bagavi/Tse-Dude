import CommonFunctions, numpy

def AnalyzeIIDMarkovData(markovTransitionProbab = .9):
    Array = CommonFunctions.FiletoArray('ZIIDMarkovResults_posix.05.csv', Int=True)
    ReadArray = []
    for row in Array:
        if row[3] == markovTransitionProbab:
            ReadArray += [row]
    ReadArray.sort( key = lambda x: [ x[2] , x[-1]])
    ContextCol = list( set( list( numpy.array(ReadArray)[:,2] ) ) )
    ContextCol.sort()
    RatioCol   = list( set( list( numpy.array(ReadArray)[:,-1] ) ) )
    RatioCol.sort()
    
    DataMatrix = numpy.zeros( ( len(RatioCol) + 1 , len(ContextCol) + 1 ))
    for row in ReadArray:
        DataMatrix[ int( RatioCol.index(row[-1] ) ) + 1 ][ int( row[2] ) ] = row[-2]
#         print(row)
#         print (DataMatrix)
    DataMatrix[0] = [-1] + ContextCol
    DataMatrix[:,0] = [-1] + RatioCol
    print( DataMatrix )
    CommonFunctions.WriteArrayinFile(DataMatrix, "Draw_IId_Markov.csv")
    print( "DONE")
    
AnalyzeIIDMarkovData( markovTransitionProbab = .97)    
