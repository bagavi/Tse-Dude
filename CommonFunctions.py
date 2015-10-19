import random
import numpy, csv, os
from collections import OrderedDict
import SimpleDude

def CdfFromPdf( Pdf ):
    Cdf = [ Pdf[0] ]
    for index, value in enumerate( Pdf[1:] ): 
        Cdf.append( Cdf[index] + value )
    return( Cdf )

def SampleDistributionFromCdf( Cdf, Symbols):
    TempRandom = random.random()
    for index, value in enumerate( Cdf ):
        if( TempRandom <= value):
            return( Symbols[ index ])


def SampleDistributionFromPdf( Pdf, Symbols):
    Cdf = CdfFromPdf( tuple( Pdf ) )
    return( SampleDistributionFromCdf(Cdf, Symbols))

def MatrixFromDict( Dict ):
    TMatrix = []
    for i in Dict:
        TMatrix.append( list( Dict[i].values() ) )
    return( numpy.array( TMatrix ) )

def InverseMatrix( Matrix ):
    InvMatrix = numpy.linalg.inv( Matrix )
    return( InvMatrix )
                   
def MultiplyVectorsComponenetWise( Vector1, Vector2): 
    return( numpy.multiply( Vector1, Vector2))

def PointWiseListDifference( List1, List2):
    Temp = []
    for i in range( len( List1) ):
        if( List1[i] != List2[i] ):
            Temp.append( 1 )
        else:
            Temp.append( 0 )
    return( Temp )

def CheckProbabilitiesSumtoOne( Array ):
    for i in Array:
        if( abs( sum(i) -  1 ) > .01 ):
            print( "Probabilites not summing to one!")
            
def WriteArrayinFile( Array, Filename ):
    with open( Filename, 'w') as f:                                    
            writer = csv.writer(f)                                                       
            writer.writerows(Array)
            
def FiletoArray( Filename = 'Results_posix.csv' , Int=False):
    Array = []
    with open(Filename, 'r') as f:
        reader = csv.reader(f)
        if Int:
            for i in reader:
                try:
                    Int_i = []
                    for j in i:
                        Int_i += [ float(j)]
                    Array += [ Int_i ]
                except:
                    pass
        else:
            for i in reader:
                Array += [ i ]
        
    return(Array[1:])

def groupContexts( Dictionary, Alphabet ):
    GroupDict = dict()
    for context in Dictionary:
        value = Dictionary[context]
        ConLen = len(context)
        GroupContext = list( context[: int( (ConLen-1)/2)] ) + [ '*' ] + list( context[ int( (ConLen+1)/2) :] )
        GroupDict[ tuple( GroupContext ) ] = GroupDict.get( tuple( GroupContext ), [] ) + [value]
    return(GroupDict)

def ChangeDir():
    os.chdir("D:\Eclipse\Tse-Dude")
    
def AnalyzeContextGroupInfo( Dict ):
        Ratios = []
        for i in Dict:
            Dict[i] = [x / min(Dict[i]) for x in Dict[i]]
            Ratios += [ numpy.std( Dict[i]) ]
        Ratios.sort()
        Ratios = Ratios[::-1]
        print( "FEW STATS")
        aa = min(range(len(Ratios)), key=lambda i: abs(Ratios[i]-2))
        print(  "Good std til 2", aa,"Length",len(Ratios))
    
        aa = min(range(len(Ratios)), key=lambda i: abs(Ratios[i]-5))
#        print( Ratios[ 0: aa ])
        print(  "Good std till 5", aa,"Length",len(Ratios))  
        
def MaximumApperences( Array  ):      
    InputSequence = Array[0].InputSequence.Sequence
    SequenceLength = len( InputSequence )
    FinalOutputSequence = [ None ]*SequenceLength
    ArrayOfOutputSequence = [] 
    
    for output in Array:
        ArrayOfOutputSequence += [ output.Sequence ]
    
    ArrayOfOutputSequence = numpy.array(ArrayOfOutputSequence)
    for index in range( SequenceLength ):
        Column = list( ArrayOfOutputSequence[:,index ])
        FinalOutputSequence[index] = max( Column, key = Column.count)
    
    return(FinalOutputSequence)

def VariableContext( Array  ):      
    InputSequence = Array[0].InputSequence.Sequence
    ReceivedSequence = Array[0].ReceivedSequence
    SequenceLength = len( InputSequence )
    FinalOutputSequence = [ None ]*SequenceLength
    ArrayOfOutputSequence = [] 
    GoodEdit = 0
    BadEdit = 0
    for output in Array:
        ArrayOfOutputSequence += [ output.Sequence ]
    
    ArrayOfOutputSequence = numpy.array(ArrayOfOutputSequence)
    
    for index in range( SequenceLength ):
        Column = list( ArrayOfOutputSequence[:,index ])
        ReceivedSymbol = ReceivedSequence[ index ]
        
        # Remove the recieved symbol
        TruncatedColumn = list( filter( (ReceivedSymbol ).__ne__, Column ))
        InputSymbol = InputSequence[index]
        # Return received symbol if that was the only symbol which received
        if len( TruncatedColumn ) == 0:
            FinalOutputSequence[index] = ReceivedSymbol      
        else:
            
            OutputSymbol = max( Column, key = Column.count )
            FinalOutputSequence[index] = OutputSymbol
            
            # Other context lengths corrects the min context length output
            if( InputSymbol == OutputSymbol and InputSymbol != Column[0] ):
#                 print (" Corrected " )
#                 print ( index, ":", Column, "Input = ",InputSymbol, "Recevied=", ReceivedSymbol, "output =", OutputSymbol )
                GoodEdit += 1
            elif( InputSymbol != OutputSymbol and InputSymbol == Column[0] ):
#                 print ("Wronged" )
#                 print ( index, ":", Column, "Input = ",InputSymbol, "Recevied=", ReceivedSymbol, "output =", OutputSymbol )
                BadEdit += 1
            else:
                pass
    print( "Goodedits", GoodEdit, " BadEdits", BadEdit)
    a = input("ENTER")
    return(FinalOutputSequence)
