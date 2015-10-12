import random
import numpy, csv

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
def FiletoArray( Filename = 'Results_posix.csv' ):
    Array = []
    with open(Filename, 'r') as f:
        reader = csv.reader(f)
        for i in reader:
            Array += [ i ]
    
    return(Array[1:])
