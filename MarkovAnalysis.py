import CommonFunctions

def AnalyzeMarkovData( FlipProbab , Filename ):
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
    CommonFunctions.WriteArrayinFile(Data, 'Draw_Markov.csv')
    print( "DONE")

AnalyzeMarkovData( .1, 'Results_test.csv')
