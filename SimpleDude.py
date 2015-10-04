from abc import ABCMeta, abstractmethod
from CommonFunctions import *
import collections
from collections import OrderedDict
import os

"""
    Generic Sequence Class. Defines generic functions on sequences
"""
class Sequence:
    __metaclass__  = ABCMeta
    Alphabet       = [] 
    SequenceLength = 0
    Sequence       = [] 
    Null = 0
    @abstractmethod
    def __init__(self): pass
    
    """
        To Do
        1) Add methods to anaLyze the sequences
        2) Add methods to modify the sequences
    """
    
    def getSequence(self):
        return self.Sequence

    def getLength(self):
        return self.SequenceLength
    
    def getDistribuitionOfSequence(self):
        Distribution = dict( collections.Counter( self.Sequence ))
        for i in Distribution:
            Distribution[i] = Distribution[i]/self.SequenceLength
        
        return(Distribution)

"""
    This class represents a generic input sequence. It is inherited from Sequence Class
"""
class InputSequence( Sequence ):
    # The list of symbols in the input sequence
    
    # Object Initialization
    def __init__(self, Alphabet, SequenceLength, Null = 0 ):
        self.Alphabet = Alphabet
        self.SequenceLength = SequenceLength
        self.Null = Null
        self.Sequence = [ self.Null ] * self.SequenceLength
    
    def GenerateSequence(self): pass       

"""
    Generic OutputSequence (Decoder) class
"""
class OutputSequence( Sequence):
    
    def __init__(self, Sequence):
        self.Sequence = []
        self.ReceivedSequence = Sequence
        self.SequenceLength = len( Sequence )
        
    
    def DecodeSequence(self, Channel):
        pass

"""
    Generic Channel Class
"""
class Channel:
    
    __metaclass__  = ABCMeta
    InputSequence
    OutputSequence

    @abstractmethod
    def CorruptSignal(self ):
        pass
    
    def getInputSequence(self):
        return self.InputSequence

    def getOutputSequence(self):
        return self.OutputSequence

"""
    This class generates an IID sequence. It is inherited from the InputSequence class
"""
class IIDInputSequence( InputSequence ):
    
    AlphabetPriors = [];
    
    def __init__( self, Alphabet, SequenceLength, AlphabetPriors, Null = 0 , ):
        InputSequence.__init__( self, Alphabet, SequenceLength, Null = 0 )
        self.AlphabetPriors = AlphabetPriors
        self.GenerateSequence()
        
    # Generates the sequence
    def GenerateSequence( self ):
        print( "Generating Input Sequence" )
        if( sum( self.AlphabetPriors ) != 1 ):
            print( "Priors for the letters do not sum upto one")
        
        # Create a cdf of the alphabet priors
        Cdf_AlphabetPriors = CdfFromPdf( tuple( self.AlphabetPriors ) )
        
        #Create a random sequence
        for symbolT in range( self.SequenceLength ):
            self.Sequence[ symbolT ] = SampleDistributionFromCdf( Cdf_AlphabetPriors, self.Alphabet )

class MarkovModelSequence( InputSequence ):
    
    TransitionDictionary = OrderedDict()
    ChainWeight = []
    TransitionMatrix = []
    
    def __init__(self, Alphabet, SequenceLength, TransitionDictionary, ChainWeight ):
        InputSequence.__init__( self, Alphabet, SequenceLength, Null = 0 )
        self.TransitionDictionary = TransitionDictionary
        self.AlphabetDictionaryKeyMap = dict( zip( TransitionDictionary.keys() , 
                                                     range( 0 , len( TransitionDictionary.keys() ))))
        self.ReverseAlphabetDictionaryKeyMap = dict( zip( range( 0 , len( TransitionDictionary.keys() )),
                                                          TransitionDictionary.keys() ))
        self.TransitionMatrix = MatrixFromDict( TransitionDictionary )
        

        self.ChainWeight = numpy.array( ChainWeight )

        CheckProbabilitiesSumtoOne( self.TransitionMatrix )
        CheckProbabilitiesSumtoOne( [ self.ChainWeight ] )

        self.Sequence = []
        self.GenerateSequence()
    
    def GenerateSequence(self):
        print( "Generating Input Sequence" )
        self.__generateFirstFewRandomBits()
        self.__RunMarkovChainForRandomBits()
        
    def __generateFirstFewRandomBits(self):
        for j in range( len( self.ChainWeight ) ):
            self.Sequence.append( random.choice( self.Alphabet ))
    
    def __RunMarkovChainForRandomBits(self):
        
        for i in range( len( self.ChainWeight ), self.SequenceLength ):
            if i%5000 == 0:
                print( i )
            PMatrix = []
            for j in range( len( self.ChainWeight ) ):
                letter_i_minus_j = self.Sequence[ i - 1 -j ]
                number_i_minus_j = self.AlphabetDictionaryKeyMap[ letter_i_minus_j ]
                PMatrix += [ list( self.TransitionMatrix[ number_i_minus_j ] ) ]
            PMatrix = numpy.array( PMatrix )
            
            ProbVector = self.ChainWeight.dot( PMatrix )
            RandomNumber = SampleDistributionFromPdf( ProbVector, range( len(self.Alphabet )))
            self.Sequence.append(self.ReverseAlphabetDictionaryKeyMap[ RandomNumber ])
        

class BlockwiseIndependentSequence( InputSequence ):
    
    BlockSize = 15
    NumberofBlocks = 0
    NumberofRandomBlocks = 2
    Blocks = [ ]
    
    def __init__(self, Alphabet, NumberofBlocks ):
        InputSequence.__init__( self, Alphabet, self.BlockSize*NumberofBlocks, Null = 0 )
        self.NumberofBlocks = NumberofBlocks
        self.Sequence = []
        self.__generateRandomblocks()
        self.GenerateSequence()
        
    def __generateRandomblocks(self):
        for i in range( self.NumberofRandomBlocks ):
            temp = []
            for j in range( self.BlockSize ):
                temp.append( random.choice( self.Alphabet ))
            self.Blocks.append( temp )
        
    def GenerateSequence(self):
        for i in range(self.NumberofBlocks):
            self.Sequence += random.choice( self.Blocks )
    
"""
    Implements a DiscreteMemeoryChannel
"""
class DiscreteMemoryChannel( Channel ):
    
    TransitionDictionary = dict()
    
    def __init__(self, InputSequence, TransitionDictionary ):
        #Check if the dictionary is correct
        self.TransitionDictionary = TransitionDictionary
        self.InputSequence = InputSequence
        self.CorruptSignal()
    
    
    def CorruptSignal(self):
        print( "Corrupting signal :P. Stop me if you can" )
        Sequence = self.InputSequence.getSequence()
        OutputSequence = [ ]
        #print( Sequence )
        for index, symbolT in enumerate( Sequence ):
            #print ( symbolT, index, "\n")
            if index%5000 == 0:
                print( index )
            TransitionProbabilities = tuple( self.TransitionDictionary[symbolT].values() )
            #print( TransitionProbabilities )
            indexSymbol = SampleDistributionFromPdf( TransitionProbabilities, 
                                                                tuple( self.TransitionDictionary[ symbolT ].keys() ) 
                                                                 )
            OutputSequence.append( indexSymbol )
        self.OutputSequence = OutputSequence
        
    def getTransitionDict(self ):
        return self.TransitionDictionary
    
    def getInputSequence(self):
        return self.InputSequence.getSequence()
    
    def getOutputSequence(self):
        return self.OutputSequence

    def getOutputAlphabet(self):
        return self.InputSequence.Alphabet
"""
    Implements DUDE on DMC
"""
class DUDEOutputSequence( OutputSequence ):

    
    ContextLength = 3 # IF ContextLength = 5, then k = 5, 2K+1 = 11
    HashDictionary = dict()
    CorrectedByContext = 0
    SpoiltByContext = 0
    SpolitByWrongContext = 0
    passlimit = 2500
    shouldIprint = False
    def __init__(self, Channel, LossFunction, InputSequence, ContextLength = 3):
        OutputSequence.__init__( self, Channel.getOutputSequence() )
        self.Alphabet = Channel.getOutputAlphabet()
        self.InputSequence = InputSequence
        self.ContextLength = ContextLength
        #Transition matrix
        TransitionDictionary = Channel.getTransitionDict()
        self.TransitionDictionaryKeyMap = dict( zip( TransitionDictionary.keys() , 
                                                     range( 0 , len( TransitionDictionary.keys() ))))
        self.TransitionMatrix = MatrixFromDict( TransitionDictionary )
        self.InvTransitionMatrix = InverseMatrix( self.TransitionMatrix )
        
        #Loss Function
        self.LossFunction = LossFunction
        self.LossFunctionMatrix = MatrixFromDict( self.LossFunction )
        self.LossFunctionKeyMap = dict( zip( LossFunction.keys() , range( 0 , len( LossFunction.keys() ))))

        # Default initializatioon of self.Sequence
        self.Sequence = [ None ] * len( self.ReceivedSequence )
        
    # Main function of this class
    def DecodeSequence(self):
        self.__FirstPass()
        self.__SecondPass()
        self.__AddBoundaryLength()
        return( self.Sequence )
    
    # Calculates m( z^n, z_{i-1}^{i-k}, z_{i+1}^{i+k} ] [z_i ]
    def __FirstPass(self):
        print( "In First pass")
        for i in range( self.ContextLength, len( self.ReceivedSequence ) - self.ContextLength ):
            if i%(self.passlimit*10) == 0:
                print( i, "   ",)
            TWOkSequence = tuple( self.ReceivedSequence[ i - self.ContextLength : i + self.ContextLength + 1 ] )
            self.HashDictionary[ TWOkSequence ] = self.HashDictionary.get( TWOkSequence, 0) + 1
    
    def __SecondPass(self):
        print( "In Second pass")
        for i in range( self.ContextLength, len( self.ReceivedSequence ) - self.ContextLength ):
            if i%self.passlimit == 0:
                print( i, "   ",)
            self.Sequence[ i ] = self.__getTrueSymbol( i )

    def __getTrueSymbol(self, positionI):
        z_i = self.ReceivedSequence[ positionI ]
        if( z_i == None ):
            print ("WTF")
        z_1to_K = self.ReceivedSequence[ positionI - self.ContextLength  : positionI  ]
        z1toK = self.ReceivedSequence[ positionI + 1 : positionI + self.ContextLength + 1 ]
        M = OrderedDict()
#         print( "I:        ", self.InputSequence.Sequence[ positionI - self.ContextLength  : positionI + self.ContextLength + 1 ], "Answer =", self.InputSequence.Sequence[ positionI ] )
#         print( "Context = ", z_1to_K ," * ", z1toK, "Current symbol", z_i)
        for letter in self.Alphabet:
            # Fraction of context with z_1to_K + letter + z1toK
            M[ letter ]=  self.__getDictProbabilites(  z_1to_K + [ letter ] + z1toK  )
#             print( "Probab for = ",z_1to_K,  letter, z1toK, M[ letter ])
        
        mT_Pi_inv = numpy.array( list( M.values() ) ).dot( self.InvTransitionMatrix )
        minPenalty = { "letter": None, "value": numpy.Infinity }
        for letter in self.Alphabet:
            LossVector = MultiplyVectorsComponenetWise(
                                self.LossFunctionMatrix[:, self.LossFunctionKeyMap[ letter ] ],
                                self.TransitionMatrix[: ,self.TransitionDictionaryKeyMap[ z_i ] ]
                            )
            # mT_Pi_inv is P(Xt/ z^{n/t}
            Penalty = LossVector.dot(mT_Pi_inv)
#             print( "Letter and its loss function ", letter, LossVector, Penalty)
            if( minPenalty[ "value" ]  > Penalty):
                minPenalty[ "value" ]  = Penalty
                minPenalty[ "letter" ] = letter

        # Counting the different types of errors and corrections
        if( z_i == self.InputSequence.Sequence [ positionI ] and z_i != minPenalty[ "letter" ] ):
            if( self.InputSequence.Sequence[ positionI - self.ContextLength  : positionI ] == z_1to_K and
                self.InputSequence.Sequence[ positionI + 1 : positionI + self.ContextLength + 1 ] == z1toK  ): 
                # implies that the context was right 
                self.SpoiltByContext += 1
            else:
                self.SpolitByWrongContext += 1
        elif( z_i != self.InputSequence.Sequence [ positionI ] and minPenalty[ "letter" ] == self.InputSequence.Sequence[ positionI ] ):
            self.CorrectedByContext += 1

        # Debugging tool START
        if( z_i == self.InputSequence.Sequence [ positionI ] and z_i != minPenalty[ "letter" ] and self.shouldIprint):
            print("##################################################################################################")
            print( "( ", positionI, ")", "WTF, the algorithm changed the right symbol ", z_i, "to ", minPenalty[ "letter" ] )
            print( "I:        ", self.InputSequence.Sequence[ positionI - self.ContextLength  : positionI + self.ContextLength + 1 ], )
            print( "Context = ", z_1to_K ," * ", z1toK, "Current symbol", z_i)
            for letter in self.Alphabet:
                # Fraction of context with z_1to_K + letter + z1toK
                M[ letter ]=  self.__getDictProbabilites(  z_1to_K + [ letter ] + z1toK  )
                print( "Probab for = ",z_1to_K,  letter, z1toK, M[ letter ])
            print("***********************************")
            x = self.__printDictionaryValues(self.InputSequence.Sequence[ positionI - self.ContextLength  : positionI ], z_i,
                                        self.InputSequence.Sequence[ positionI + 1 : positionI + self.ContextLength + 1 ] ,self.Alphabet)
            if( self.InputSequence.Sequence[ positionI - self.ContextLength  : positionI ] == z_1to_K and
                self.InputSequence.Sequence[ positionI + 1 : positionI + self.ContextLength + 1 ] == z1toK and self.shouldIprint ): 
                # implies that the context was right 
                print("%%%%%%%%%%%%%%%%%%%%%%%%%% Right Context but Spoilt %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            else:
                print("%%%%%%%%%%%%%%%%%%%%%%%%%% Wrong Context and Spoilt %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            print("##################################################################################################")
            #Enter = input("Test")
               
        elif( z_i != self.InputSequence.Sequence [ positionI ] and minPenalty[ "letter" ] == self.InputSequence.Sequence[ positionI ] and self.shouldIprint ):
            print("##################################################################################################")
            print( "!!!!!!!!!!, the algorithm did the right thing ", z_i, "to ", minPenalty[ "letter" ] )
            print( "I:        ", self.InputSequence.Sequence[ positionI - self.ContextLength  : positionI + self.ContextLength + 1 ], )
            print( "Context = ", z_1to_K ," * ", z1toK, "Current symbol", z_i)
            for letter in self.Alphabet:
                # Fraction of context with z_1to_K + letter + z1toK
                M[ letter ]=  self.__getDictProbabilites(  z_1to_K + [ letter ] + z1toK )
                print( "Probab for = ",z_1to_K,  letter, z1toK, M[ letter ])
            print("##################################################################################################")
            print("%%%%%%%%%%%%%%%%%%%%%%%%%% Corrected %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        elif ( minPenalty[ "letter" ] != self.InputSequence.Sequence [ positionI ] and self.shouldIprint  and 
                self.InputSequence.Sequence[ positionI - self.ContextLength  : positionI ] == z_1to_K and #Enforcing same context
                self.InputSequence.Sequence[ positionI + 1 : positionI + self.ContextLength + 1 ] == z1toK ):
            print( positionI, "  !!!!!!!!!!, No change by the algo",  ". Our algo =", minPenalty[ "letter" ], "Received letter", z_i)
            print( "I:        ", self.InputSequence.Sequence[ positionI - self.ContextLength  : positionI + self.ContextLength + 1 ], )
            print( "Context = ", z_1to_K ," * ", z1toK)
       
            self.__printDictionaryValues( z_1to_K, z_i, z1toK,  [  self.InputSequence.Sequence[ positionI ], minPenalty[ "letter" ] ] )
            print("##################################################################################################")
            if os.name == "posix":  
                Enter = str( input("Enter something!!") )
           
        
        #debugging tool END
        return( minPenalty[ "letter" ] )
    
    def __AddBoundaryLength(self):
        self.Sequence = self.ReceivedSequence[: self.ContextLength ] + self.Sequence[ self.ContextLength : len(self.ReceivedSequence) - self.ContextLength ] + self.ReceivedSequence [ len(self.ReceivedSequence) - self.ContextLength: ]
    
    def __IncreamentDictElement(self, key ):
        self.HashDictionary[ key  ] = self.HashDictionary.get(key, 0) + 1
        
    def __getDictProbabilites(self, key ):
        return( self.HashDictionary.get( tuple(key), 0) )
    
    #Debuggin Tool
    def __printDictionaryValues(self, pre, z_i,post, Alphabet ):
        M = {}
        for letter in self.Alphabet:
            # Fraction of context with z_1to_K + letter + z1toK
            M[ letter ] =  self.__getDictProbabilites(  pre + [ letter ] + post  )
            if( letter in Alphabet ):
                print( "Probab for = ",pre,  letter, post, M [ letter ] )

        mT_Pi_inv = numpy.array( list( M.values() ) ).dot( self.InvTransitionMatrix )
        minPenalty = { "letter": None, "value": numpy.Infinity }
        for letter in Alphabet:
            LossVector = MultiplyVectorsComponenetWise(
                                self.LossFunctionMatrix[:, self.LossFunctionKeyMap[ letter ] ],
                                self.TransitionMatrix[: ,self.TransitionDictionaryKeyMap[ z_i ] ]
                            ) 
            Penalty = LossVector.dot(mT_Pi_inv)
            print( "Loss function matrix", self.LossFunctionMatrix, "\n")
            print( "Transition Matrix", self.TransitionMatrix, "\n")
            print( "matrix", mT_Pi_inv)
            print( "Letter, its loss function, Transition Column ", letter,  self.LossFunctionMatrix[:, self.LossFunctionKeyMap[ letter ] ],  self.TransitionMatrix[: ,self.TransitionDictionaryKeyMap[ letter ] ]
                                )
            print( "Penalty", Penalty)
            if( minPenalty[ "value" ]  > Penalty):
                minPenalty[ "value" ]  = Penalty
                minPenalty[ "letter" ] = letter
        
        print( minPenalty )
        return( minPenalty[ "letter"])

# Parameters of the whole system
Length = 20000

p1 = 0.9
p2 = ( 1 - p1 )/3
TransitionDictionary = OrderedDict( { 'A' : OrderedDict( {'A':p1, 'G':p2, 'T':p2, 'C':p2} ),
                         'G' : OrderedDict( {'A':p2, 'G':p1, 'T':p2, 'C':p2} ),
                         'T' : OrderedDict( {'A':p2, 'G':p2, 'T':p1, 'C':p2} ),
                         'C' : OrderedDict( {'A':p2, 'G':p2, 'T':p2, 'C':p1} )
                        } )
Alphabet =  list( TransitionDictionary.keys() )
AlphabetPriors = [0.2,0.3,0.3,.2]
l1 = 10
l2 = 0.01
LossFunction = OrderedDict ( 
               { 'A' : OrderedDict( {'A':l2, 'G':l1, 'T':l1, 'C':l1} ),
                 'G' : OrderedDict( {'A':l1, 'G':l2, 'T':l1, 'C':l1} ),
                 'T' : OrderedDict( {'A':l1, 'G':l1, 'T':l2, 'C':l1} ),
                 'C' : OrderedDict( {'A':l1, 'G':l1, 'T':l1, 'C':l2} )
            })
# Running Functions
#InputTest = IIDInputSequence( Alphabet, Length, AlphabetPriors )
#InputTest = BlockwiseIndependentSequence( Alphabet, 5000 )
q1 = .25
q2 = .3
q3 = .15
MarkovSequenceLength = 1000*5
MarkovTransitionDictionary = OrderedDict( { 'A' : OrderedDict( {'A':q1, 'G':q2, 'T':q2, 'C':q3} ),
                                      'G' : OrderedDict( {'A':q2, 'G':q1, 'T':q2, 'C':q3} ),
                                      'T' : OrderedDict( {'A':q3, 'G':q2, 'T':q1, 'C':q2} ),
                                    'C' : OrderedDict( {'A':q3, 'G':q2, 'T':q2, 'C':q1} )
                                    } )
ChainWeight = [.4, .25 , .2 , .1 , .05]
ContextLength = 3

print( "Sequence Length for Markov (if applicable) ", MarkovSequenceLength)
print( "Flip probability of DMC ", ( 1- p1))
print( "Dude Loss dictionary", LossFunction)
print( "DUDE context length" , ContextLength)

#Calling the functions
InputTest = MarkovModelSequence( Alphabet, MarkovSequenceLength, MarkovTransitionDictionary, ChainWeight)
ChannelTest = DiscreteMemoryChannel( InputTest, TransitionDictionary )
OutputTest = DUDEOutputSequence( ChannelTest, LossFunction, InputTest , ContextLength = ContextLength)
OutputTest.DecodeSequence()

# Done with calling functions
Input = InputTest.getSequence()
Received = OutputTest.ReceivedSequence
Corrected = OutputTest.Sequence


z = PointWiseListDifference( Input, Received)
print( "Changes made by channel", sum(z))
z = PointWiseListDifference( Input, Corrected)
print( "Difference between actual and corrected sequence", sum( z ) )
z = PointWiseListDifference( Received, Corrected)
print( "Difference between received and corrected sequence",sum( z ) )
print( "Correct changes Made by the right context", OutputTest.CorrectedByContext)
print( "Number of spoils by the right context", OutputTest.SpoiltByContext)
print( "Number of spoils by the wrong context", OutputTest.SpolitByWrongContext)
