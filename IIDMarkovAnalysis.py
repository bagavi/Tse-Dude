import CommonFunctions, numpy

def AnalyzeIIDMarkovData(markovTransitionProbab = -1, col = -1):
    Array = CommonFunctions.FiletoArray('FakeResults_reads_simulation__posix.csv', Int=True)
#    Array = CommonFunctions.FiletoArray('WOW.csv', Int=True)
#     Array = CommonFunctions.FiletoArray('ZIIDMarkovResults_posix.csv', Int=True)
#     Array = CommonFunctions.FiletoArray('bc.csv', Int=True)
    ReadArray = []
    for row in Array:
        if row[3] == markovTransitionProbab:
            ReadArray += [row]
        else:
            pass
    RatioNumber = - 2
    ColumnNumber = 2
    ReadArray.sort( key = lambda x: [ x[2] , x[-1]])
    ContextCol = list( set( list( numpy.array(ReadArray)[:,ColumnNumber] ) ) )
    ContextCol.sort()
    RatioCol   = list( set( list( numpy.array(ReadArray)[:, RatioNumber] ) ) )
    RatioCol.sort()
    
    DataMatrix = numpy.zeros( ( len(RatioCol) + 1 , len(ContextCol) + 1 ))
    for row in ReadArray:
        DataMatrix[ int( RatioCol.index(row[RatioNumber] ) ) + 1 ][ int( ContextCol.index( row[ColumnNumber]  ) ) + 1 ] = row[col]
#         print(row)
#         print (DataMatrix)
    DataMatrix[0] = [-1] + ContextCol
    DataMatrix[:,0] = [-1] + RatioCol
    print( DataMatrix )
    CommonFunctions.WriteArrayinFile(DataMatrix, "Draw_IId_Markov.csv")
    print( "DONE")
    
# col = -2 for iidmarkov
AnalyzeIIDMarkovData( markovTransitionProbab = -1, col = -3)    
