import os, csv, numpy, math
from _csv import reader
import CommonFunctions


def RestructureData( FlipProbab , Filename ):
    Results = CommonFunctions.FiletoArray(Filename)
    Data = [ [ '*' ]]
    RowSize = 0
    ColumnSize = 1
    minContextLength = 1000
    
    for i in Results:
        
        FlipProbab_i = float( i[1] )
        if FlipProbab != FlipProbab_i:
            continue
        
        TransitionProbab = float(i[3])
        try:
            Data[0].index(TransitionProbab, )
        except:
            ColumnSize += 1
            Data[0].append(TransitionProbab)
        Context = int( i[2] )
        if Context < minContextLength:
            minContextLength = Context
        if RowSize < Context:
            RowSize = Context

    for i in range( RowSize ):
        Data.append( [i+minContextLength]+[0]*(ColumnSize) )
    
    for i in Results:
        InputSize = i[0]
        FlipProbab_i = float( i[1] )
        if FlipProbab != FlipProbab_i:
            continue
        Context = int( i[2] ) 
        TransitionProbab = float(i[3])
        try:
            TotalChanges = float(i[7])
        except:
            pass
        try:
            Correctchanges = float(i[8])
        except:
            pass
        try:
            index = Data[0].index(TransitionProbab)
        except:
            pass
        Data[Context - minContextLength + 1][index] = TotalChanges
    print (Data)
    CommonFunctions.WriteArrayinFile(Data, 'Draw_results_1.csv')
    print( "DONE")

    
def AnalyseLengthSimData(ProbRange = [ .9 ]):
    ReadArray = CommonFunctions.FiletoArray('Results_length.csv', Int=True)
    """
    Sorting Order
    
    !)Length
    2)Error Probab
    3)MarkovTransitionProbab
    
    """
    
    
    for row in ReadArray:
        row[1] = int( math.ceil(row[1]*10 ))
        row[2] = int( math.ceil(row[2]*10 ))
        row[3] = int( math.ceil(row[3]*10 ))
    
    ReadArray.sort( key = lambda x: [ x[0], x[3], x[2] ])
    MergedArray = []
    # Merging similar rows
    
    #Equality function
    i= 1
    prevRow = ReadArray[0]
    i_start = 0
    while( i < len(ReadArray) ):
        curRow = ReadArray[i]
        
        if( curRow[0] == prevRow[0] and curRow[1] == prevRow[1] and curRow[2] == prevRow[2] and curRow[3] == prevRow[3] ):
            i += 1
        else:
            MergedArray += [ list( numpy.average(ReadArray[i_start :i], axis = 0) )]
            prevRow = curRow
            i_start = i
    
    #sorting array by length
    MergedArray.sort(key=lambda x: [ x[2], x[3], x[0]], reverse=False)
    FirstCol = list( numpy.array(MergedArray)[:,0] )
    # Number of lenghts
    NoOfLength = FirstCol[FirstCol.index(100)+1:].index(100) - FirstCol.index(100) + 1
    
    CommonFunctions.WriteArrayinFile(MergedArray, "Test.csv")
    a = 10
    
RestructureData( .1, 'Results_negative1.csv')
#AnalyseLengthSimData([.9])