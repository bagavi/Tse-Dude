import CommonFunctions, numpy
from operator import itemgetter

def AlphaAnalysis( RContextLength = 6 ):
    Array = CommonFunctions.FiletoArray('YTrueFakeResults_reads_simulation__posix2.csv', Int=True)
    Dictionary = dict()
    ReadArray = []
    for row in Array:
        alpha = int(row[-1])
        CoverageDepth = int(row[-3])
        ContextLength = int(row[2])
        key = (alpha, CoverageDepth, ContextLength )
        NetCorrections = float(row[-4])
        Changes = float( row[-6] )
        WrongCorrections = float( row[-6]) - float(row[-5])
        data = [NetCorrections ]#, Changes, WrongCorrections]
        Dictionary[ key ] = Dictionary.get( key, []) + [ data ]
    
    DataArray = []
    for i in Dictionary:
        DataArray += [ list( numpy.append( numpy.array(list(i))  , numpy.average(numpy.array( Dictionary[i] ), 0 ) ) )]
    DataArray.sort( key = itemgetter(1) ) # Sorted w.r.t C D
    DataArray.sort( key = itemgetter(0) ) # Sorted w.r.t Alpha
    DataArray.sort( key = itemgetter(2) ) # Sorted w.r.t C.L
    
    FilteredDataArray = [  row for row in DataArray if(row[2] == RContextLength) ]
    FilteredDataArray.sort(key=itemgetter(1), reverse=True)
    for i in FilteredDataArray:
        print(i)
    print( "hi" )
    
    Alpha0Array = [  row for row in DataArray if(row[0] == 0) ]
    Alpha0Array.sort(key=itemgetter(1), reverse=True)
    Alpha0Array.sort(key=itemgetter(0), reverse=True)
    for i in Alpha0Array:
        print(i)
    
    print( "\n\n")
    DataArray.sort( key = itemgetter(3), reverse = True)
    for i in DataArray[:100]:
        print(i)
AlphaAnalysis( )    
