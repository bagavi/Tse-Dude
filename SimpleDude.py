"""
 This script implements three types of classes.
 
 1)Input Class - This class can generates inputs in different ways eg. IId, blockwise, markov
 2)Channel Class - This class modifies a input sequence according to the channel property. Eg. BSC, Erasure
 3)Output Class - This implements the output decoder. Eg DUDE 
"""

from abc import ABCMeta, abstractmethod
from CommonFunctions import *
import math, collections
from Bio import SeqIO


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
    
    def InitializeSequence(self, Sequence ):
        self.Sequence = Sequence

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
        for symbolT in range( int( self.SequenceLength ) ):
            self.Sequence[ symbolT ] = SampleDistributionFromCdf( Cdf_AlphabetPriors, self.Alphabet )

class ReadFromReads( InputSequence ):
    filename = ""
    
    def __init__(self, filename, NoOfReads):
        self.filename = filename
        self.Sequence = []
        self.NoOfReads = NoOfReads
        self.GenerateSequence()
        self.Alphabet = [ 'A', 'C', 'T', 'G']
        
    def GenerateSequence(self):
        handle = open(self.filename)
        i = 0
        for seq_record in SeqIO.parse( handle, "fastq") :
            if 'N' in list( seq_record.seq ): # Ignoring the reads which have 'N'.
                continue
            if( i  == self.NoOfReads ):
                break
            i += 1
            self.Sequence += list(seq_record.seq)
        
class ReadInputFromFile( InputSequence ):
    
    filename = ""
    
    def __init__(self, filename):
        self.filename = filename
        self.Sequence = []
        self.GenerateSequence()

    def GenerateSequence(self):
        handle = open(self.filename)
        for seq_record in SeqIO.parse( handle, "fasta"):
            print( seq_record.id )    
            self.Sequence += str(  seq_record.seq )
        self.Sequence = list(filter( ('R').__ne__, self.Sequence ) )
        self.Alphabet = list( set( self.Sequence ) )
        
        # REMOVE THIS
        self.Sequence = self.Sequence[:10000]

class MarkovModelSequence( InputSequence ):
    
    TransitionDictionary = OrderedDict()
    ChainWeight = []
    TransitionMatrix = []
    
    def __init__(self, Alphabet, SequenceLength, TransitionDictionary, ChainWeight ):
        InputSequence.__init__( self, Alphabet, SequenceLength, Null = 0 )
        
        # Initializing the initial variables of the class
        self.TransitionDictionary = TransitionDictionary
        self.AlphabetDictionaryKeyMap = dict( zip( TransitionDictionary.keys() , range( 0 , len( TransitionDictionary.keys() ))))
        self.ReverseAlphabetDictionaryKeyMap = dict( zip( range( 0 , len( TransitionDictionary.keys() )), TransitionDictionary.keys() ))
        self.TransitionMatrix = MatrixFromDict( TransitionDictionary )
        self.ChainWeight = numpy.array( ChainWeight )
        self.Sequence = []
        
        # Sanity checks
        CheckProbabilitiesSumtoOne( self.TransitionMatrix )
        CheckProbabilitiesSumtoOne( [ self.ChainWeight ] )
        
        # Main function
        self.GenerateSequence()
    
    def GenerateSequence(self):
        print( "Generating Input Sequence" )
        self.__generateFirstFewRandomBits()
        self.__RunMarkovChainForRandomBits()
        
    def __generateFirstFewRandomBits(self):
        for j in range( len( self.ChainWeight ) ):
            self.Sequence.append( random.choice( self.Alphabet ))
    
    def __RunMarkovChainForRandomBits(self):
        
        for i in range( len( self.ChainWeight ), int( self.SequenceLength ) ):
            if i%50000 == 0:
                print( i )
            PMatrix = []
            for j in range( len( self.ChainWeight ) ):
                letter_i_minus_j = self.Sequence[ i - 1 -j ]
                number_i_minus_j = self.AlphabetDictionaryKeyMap[ letter_i_minus_j ]
                PMatrix         += [ list( self.TransitionMatrix[ number_i_minus_j ] ) ]
            PMatrix = numpy.array( PMatrix )
            
            ProbVector   = self.ChainWeight.dot( PMatrix )
            RandomNumber = SampleDistributionFromPdf( ProbVector, range( len(self.Alphabet )))
            self.Sequence.append(self.ReverseAlphabetDictionaryKeyMap[ RandomNumber ])
        
class IIDandMarkovSequence( InputSequence ):
    
    MarkovRatio = .7
    IIDRatio = 1 - MarkovRatio
    
    def __init__(self, Alphabet, MarkovRatio, Length, MarkovTransitionDictionary):
        InputSequence.__init__(self, Alphabet, Length, Null = 0)
        self.MarkovRatio = MarkovRatio
        self.IIDRatio = 1 - MarkovRatio
        self.MarkovLength = Length*self.MarkovRatio
        self.IIDLength = Length - self.MarkovLength
        self.MarkovTransitionDictionary = MarkovTransitionDictionary
        self.Sequence = []
        self.GenerateSequence()
        
    def GenerateSequence(self):
        MarkovSequence = MarkovModelSequence( self.Alphabet, self.MarkovLength, self.MarkovTransitionDictionary, [1])
        IIDSequence = IIDInputSequence( self.Alphabet, self.IIDLength, [ .25 ]*4)
        self.Sequence = MarkovSequence.Sequence + IIDSequence.Sequence
#         self.Sequence = MarkovSequence.Sequence[: len(MarkovSequence)/2 ] + IIDSequence.Sequence +MarkovSequence.Sequence[ len(MarkovSequence)/2: ]
        
        
class BlockwiseIndependentSequence( InputSequence ):
    
    BlockSize            = 15
    NumberofBlocks       = 0
    NumberofRandomBlocks = 2
    Blocks               = []
    
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
        Sequence = self.InputSequence.Sequence
        OutputSequence = [ ]
        self.Changes = { 'A': 0, 'C': 0, 'T':0, 'G':0 }
        #print( Sequence )
        for index, symbolT in enumerate( Sequence ):
            #print ( symbolT, index, "\n")
            if index%50000 == 0:
                print( index )
            if symbolT in self.InputSequence.Alphabet:
                TransitionProbabilities = tuple( self.TransitionDictionary[symbolT].values() )
                indexSymbol = SampleDistributionFromPdf( TransitionProbabilities, tuple( self.TransitionDictionary[ symbolT ].keys() ) )
                OutputSequence.append( indexSymbol )
                if indexSymbol != symbolT:
                    self.Changes[symbolT] += 1
            else:
                OutputSequence.append( symbolT )
        self.OutputSequence = OutputSequence
        print( "Total Changes ", self.Changes)
        
    def getTransitionDict(self ):
        return self.TransitionDictionary
    
    def getInputSequence(self):
        return self.InputSequence.getSequence()
    
    def getOutputSequence(self):
        return self.OutputSequence

    def getOutputAlphabet(self):
        return self.InputSequence.Alphabet


class ReadsInput( InputSequence ):
    
    #Array of InputSequences
    Reads = []
    
    def __init__(self, InputSequence, ReadSize, CoverageDepth = 5):
        self.InputSequence = InputSequence
        self.Alphabet = InputSequence.Alphabet
        self.ReadSize = ReadSize
        self.NumberofReads = math.ceil( len( self.InputSequence.Sequence )*CoverageDepth / self.ReadSize )
        self.Sequence = []
        self.GenerateReads()
        a = 10
    
    def GenerateReads(self):
        Sequence = []
        for i in range( self.NumberofReads ):
            RandomIndex = random.randint( 0, len( self.InputSequence.Sequence ) )
            SingleRead = self.InputSequence.Sequence[ RandomIndex: RandomIndex + self.ReadSize ]
            self.Sequence += SingleRead
        
"""
    Implements DUDE on DMC
"""
class DUDEOutputSequence( OutputSequence ):

    # Context length pf the context matching string
    ContextLength = 3 # IF ContextLength = 5, then k = 5, 2K+1 = 11
    
    # This is a hash table which stores number of times each context has been repeated
    HashDictionary = dict()
    
    #Stores the number of times the given algo has made a right correction
    CorrectedByContext = 0
    
    #Number of times the algo replaced a right symbol with a wrong one ( even though the conext was right)
    SpoiltByContext = 0
    
    #Number of times the algo replaced a right symbol with a wrong one ( because of the wrong context)
    SpolitByWrongContext = 0
    #
    Nochangesmade = 0
    #print limit (ignore this)
    passlimit = 25000
    shouldIprint = False
    
    def __init__(self, Channel, LossFunction, InputSequence, ContextLength = 3, shouldIprint = False):
        OutputSequence.__init__( self, Channel.getOutputSequence() )
        self.Alphabet = Channel.getOutputAlphabet()
        self.InputSequence = InputSequence
        self.ContextLength = ContextLength
        self.shouldIprint = shouldIprint
    
        #Transition matrix
        TransitionDictionary = Channel.getTransitionDict()
        self.TransitionDictionaryKeyMap = dict( zip( TransitionDictionary.keys(), range(0 , len(TransitionDictionary.keys()))))
        self.TransitionMatrix = MatrixFromDict( TransitionDictionary )
        self.InvTransitionMatrix = InverseMatrix( self.TransitionMatrix )
        
        #Loss Function
        self.LossFunction = LossFunction
        self.LossFunctionMatrix = MatrixFromDict( self.LossFunction )
        self.LossFunctionKeyMap = dict( zip( LossFunction.keys(), range( 0 , len(LossFunction.keys()))))

        # Default initializatioon of self.Sequence
        self.Sequence = [ None ] * len( self.ReceivedSequence )
        self.DecodeSequence()
    # Main function of this class
    def DecodeSequence(self):
        self.__FirstPass()
        self.__SecondPass()
        self.__AddBoundaryLength()
        return( self.Sequence )
    
    def __AddBoundaryLength(self):
        self.Sequence = self.ReceivedSequence[: self.ContextLength ] + self.Sequence[ self.ContextLength : len(self.ReceivedSequence) - self.ContextLength ] + self.ReceivedSequence [ len(self.ReceivedSequence) - self.ContextLength: ]
    
    def __IncreamentDictElement(self, key ):
        self.HashDictionary[ key  ] = self.HashDictionary.get(key, -1) + 1 # Here minus -1 is used to ignore the first observation
        
    def __getDictProbabilites(self, key ):
        return( self.HashDictionary.get( tuple(key), 0) ) 
    
    # Calculates m( z^n, z_{i-1}^{i-k}, z_{i+1}^{i+k} ] [z_i ]
    def __FirstPass(self):
        print( "In First pass")
        for i in range( self.ContextLength, len( self.ReceivedSequence ) - self.ContextLength ):
            if i%(self.passlimit*10) == 0:
                print(i, " ", self.SequenceLength,"Context length", self.ContextLength)
            TWOkSequence = tuple( self.ReceivedSequence[ i - self.ContextLength : i + self.ContextLength + 1 ] )
            self.HashDictionary[ TWOkSequence ] = self.HashDictionary.get( TWOkSequence, 0) + 1
    
    def __SecondPass(self):
        print( "In Second pass")
        for i in range( self.ContextLength, len( self.ReceivedSequence ) - self.ContextLength ):
            if i%self.passlimit == 0:
                print(i, " ", self.SequenceLength,"Context length", self.ContextLength)
            self.Sequence[ i ] = self.__getTrueSymbol( i )

    def __getTrueSymbol(self, positionI):
        z_i = self.ReceivedSequence[ positionI ]
        if z_i not in self.Alphabet:
            pass
        #If the alphabet is not among ACGT, we dont "correct" it
        # Initializing pre and post context sequence variables
        z_1to_K = self.ReceivedSequence[ positionI - self.ContextLength  : positionI  ]
        z1toK = self.ReceivedSequence[ positionI + 1 : positionI + self.ContextLength + 1 ]
        
        M = OrderedDict()
#         print( "I:        ", self.InputSequence.Sequence[ positionI - self.ContextLength  : positionI + self.ContextLength + 1 ], "Answer =", self.InputSequence.Sequence[ positionI ] )
#         print( "Context = ", z_1to_K ," * ", z1toK, "Current symbol", z_i)
        for letter in self.Alphabet:
            # Fraction of context with z_1to_K + letter + z1toK
            M[ letter ]=  self.__getDictProbabilites(  z_1to_K + [ letter ] + z1toK  )
#             print( "Probab for = ",z_1to_K,  letter, z1toK, M[ letter ])
        if len(M) > 4:
            pass
        mT_Pi_inv = numpy.array( list( M.values() ) ).dot( self.InvTransitionMatrix )
        minPenalty = { "letter": None, "value": numpy.Infinity }
        for letter in self.Alphabet:
            if z_i in self.Alphabet:
                lambda_zi = self.TransitionMatrix[:, self.TransitionDictionaryKeyMap[ z_i ] ]
            else:
                lambda_zi = numpy.array( [ 1, 1, 1, 1])
            LossVector = MultiplyVectorsComponenetWise(
                                self.LossFunctionMatrix[:, self.LossFunctionKeyMap[ letter ] ],
                                lambda_zi
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
            
        elif ( minPenalty[ "letter" ] != self.InputSequence.Sequence [ positionI ] and self.shouldIprint  and 
                self.InputSequence.Sequence[ positionI - self.ContextLength  : positionI ] == z_1to_K and #Enforcing same context
                self.InputSequence.Sequence[ positionI + 1 : positionI + self.ContextLength + 1 ] == z1toK ):
            self.Nochangesmade += 1
        if( self.shouldIprint(z_i, self.Alphabet) ):
            self.__debuggingSection(z_i, z_1to_K, z1toK, positionI, minPenalty, M)
        #debugging tool END
        return( minPenalty[ "letter" ] )

    
    """
        This function is very ugly. This basically prints stuff if required
    """    
    def __debuggingSection(self, z_i, z_1to_K, z1toK, positionI, minPenalty, M):
        # Debugging tool START
        if( z_i == self.InputSequence.Sequence [ positionI ] and z_i != minPenalty[ "letter" ] ):
            print("##################################################################################################")
            print( "( ", positionI, ")", "WTF, the algorithm changed the right symbol ", z_i, "to ", minPenalty[ "letter" ] )
            print( "I:  8      ", self.InputSequence.Sequence[ positionI - self.ContextLength  : positionI + self.ContextLength + 1 ], )
            print( "Context = ", z_1to_K ," * ", z1toK, "Current symbol", z_i)
            for letter in self.Alphabet:
                # Fraction of context with z_1to_K + letter + z1toK
                M[ letter ]=  self.__getDictProbabilites(  z_1to_K + [ letter ] + z1toK  )
                print( "Probab for = ",z_1to_K,  letter, z1toK, M[ letter ])
            print("***********************************")
#             self.__printDictionaryValues(self.InputSequence.Sequence[ positionI - self.ContextLength  : positionI ], z_i,
#                                         self.InputSequence.Sequence[ positionI + 1 : positionI + self.ContextLength + 1 ] ,self.Alphabet)
            if( self.InputSequence.Sequence[ positionI - self.ContextLength  : positionI ] == z_1to_K and
                self.InputSequence.Sequence[ positionI + 1 : positionI + self.ContextLength + 1 ] == z1toK and self.shouldIprint ): 
                # implies that the context was right 
                print("%%%%%%%%%%%%%%%%%%%%%%%%%% Right Context but Spoilt %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            else:
                print("%%%%%%%%%%%%%%%%%%%%%%%%%% Wrong Context and Spoilt %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            print("##################################################################################################")
            if os.name == "posix":  
                 Enter = str( input("Enter something!!") )               

        elif( z_i != self.InputSequence.Sequence [ positionI ] and minPenalty[ "letter" ] == self.InputSequence.Sequence[ positionI ] and False ):
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
            if os.name == "posix":  
                 self.Enter = str( input("Enter something!!") )               

        elif ( minPenalty[ "letter" ] != self.InputSequence.Sequence [ positionI ] and self.shouldIprint  and 
                self.InputSequence.Sequence[ positionI - self.ContextLength  : positionI ] == z_1to_K and #Enforcing same context
                self.InputSequence.Sequence[ positionI + 1 : positionI + self.ContextLength + 1 ] == z1toK and False):
            print( positionI, "  !!!!!!!!!!, No change by the algo",  ". Our algo =", minPenalty[ "letter" ], "Received letter", z_i)
            print( "I:        ", self.InputSequence.Sequence[ positionI - self.ContextLength  : positionI + self.ContextLength + 1 ], )
            print( "Context = ", z_1to_K ," * ", z1toK)
        
            self.__printDictionaryValues( z_1to_K, z_i, z1toK,  [ self.InputSequence.Sequence[ positionI ] ]+ list( set( [ minPenalty[ "letter" ], z_i ] ) ) )
            print("##################################################################################################")
            if os.name == "posix":  
                Enter = str( input("Enter something!!") )
            
         
    
    #Debuggin Tool
    def __printDictionaryValues(self, pre, z_i, post, Alphabet ):
        M = {}
        for letter in self.Alphabet:
            # Fraction of context with z_1to_K + letter + z1toK
            M[ letter ] =  self.__getDictProbabilites(  pre + [ letter ] + post  )
            if( letter in Alphabet ):
                print( "Probab for = ",pre,  letter, post, M [ letter ] )

        mT_Pi_inv = numpy.array( list( M.values() ) ).dot( self.InvTransitionMatrix )
        minPenalty = { "letter": None, "value": numpy.Infinity }
        print( "Transition Matrix", self.TransitionMatrix, "\n")
        for letter in Alphabet: 
            LossVector = MultiplyVectorsComponenetWise(
                                self.LossFunctionMatrix[:, self.LossFunctionKeyMap[ letter ] ],
                                self.TransitionMatrix[: ,self.TransitionDictionaryKeyMap[ z_i ] ]
                            ) 
            Penalty = LossVector.dot(mT_Pi_inv)
            print( "Loss function matrix", self.LossFunctionMatrix, "\n")
            print( "LossVector", LossVector)
            print( "Letter, its loss function, Transition Column ", letter,  self.LossFunctionMatrix[:, self.LossFunctionKeyMap[ letter ] ],  self.TransitionMatrix[: ,self.TransitionDictionaryKeyMap[ z_i ] ]
                                )
            print( "Penalty", Penalty)
            if( minPenalty[ "value" ]  > Penalty):
                minPenalty[ "value" ]  = Penalty
                minPenalty[ "letter" ] = letter
        
        print( minPenalty )
        return( minPenalty[ "letter"])

class System:
    wrongSymbolLoss = 10
    rightSymbolLoss = 0.01
    LossFunction = OrderedDict ( 
                   { 'A' : OrderedDict( {'A':rightSymbolLoss, 'G':wrongSymbolLoss, 'T':wrongSymbolLoss, 'C':wrongSymbolLoss} ),
                     'G' : OrderedDict( {'A':wrongSymbolLoss, 'G':rightSymbolLoss, 'T':wrongSymbolLoss, 'C':wrongSymbolLoss} ),
                     'T' : OrderedDict( {'A':wrongSymbolLoss, 'G':wrongSymbolLoss, 'T':rightSymbolLoss, 'C':wrongSymbolLoss} ),
                     'C' : OrderedDict( {'A':wrongSymbolLoss, 'G':wrongSymbolLoss, 'T':wrongSymbolLoss, 'C':rightSymbolLoss} )
                })
    # Input Sequence Length
    SequenceLength = 0
    ChainWeight = [1]
    ContextLength = 3
    IIDMarkovRatio = -1
    
    def __init__(self, ContextLength = -1, ContextLengthMin = 3, ContextLengthMax = 7, SequenceLength = 10000, flipProbab = .9, shouldIprint = False):
        self.ContextLengthMin = ContextLengthMin
        self.ContextLengthMax = ContextLengthMax
        self.ContextLength = ContextLength
        self.shouldIprint = shouldIprint
        self.SequenceLength = SequenceLength
        self.p = flipProbab
        p = self.p
        self.NumberOfInstances = 0
        self.TransitionDictionary = OrderedDict( { 
                                 'A' : OrderedDict( {'A':1-p, 'G':p/3, 'T':p/3, 'C':p/3} ),
                                 'G' : OrderedDict( {'A':p/3, 'G':1-p, 'T':p/3, 'C':p/3} ),
                                 'T' : OrderedDict( {'A':p/3, 'G':p/3, 'T':1-p, 'C':p/3} ),
                                 'C' : OrderedDict( {'A':p/3, 'G':p/3, 'T':p/3, 'C':1-p} )
                                } )
        self.Alphabet =  list( self.TransitionDictionary.keys() )
                
    def PrintInformation(self, Filename = 'Results_'+os.name+'.csv'):
        self.r1 = -1 #BAD CODE
        print( "Instance Number", self.NumberOfInstances)
        print( "Flip probability of DMC ", self.p)
#         print( "Dude Loss dictionary", self.LossFunction)
        print( "DUDE context length" , self.ContextLength)
#         print( "Partial Input Sequence", self.Input.getSequence()[ : 500])
        
        # Done with calling functions
        Input = self.Input.getSequence()
        Received = self.Output.ReceivedSequence
        Corrected = self.Output.Sequence
    
        z1 = PointWiseListDifference( Input, Received)
        print( "Changes made by channel", sum(z1))
        z2 = PointWiseListDifference( Input, Corrected)
        print( "Difference between actual and corrected sequence", sum( z2 ) )
        z3 = PointWiseListDifference( Received, Corrected)
        print( "Difference between received and corrected sequence",sum( z3 ) )
        print( "Correct changes Made by the right context", self.Output.CorrectedByContext)
        print( "Number of spoils by the wrong context", self.Output.SpolitByWrongContext)
        print( "Number of spoils by the right context", self.Output.SpoiltByContext)
        print( "Number of unchanged", self.Output.Nochangesmade)
        print( "Fraction of changed symbols (w.r.t no of errors)", float( sum( z3 ) )/float( sum( z1 ) + 1))
        print( "Fraction of correctly changed symbols (w.r.t no of errors)", self.Output.CorrectedByContext/float( sum( z1 ) ))
        fractionOfChanges = float( sum( z3 ) )/float( sum( z1 ) )
        fractionOfChanges = float("{0:.3f}".format( fractionOfChanges ) )
        Heading = [ "InputSequence Length", "Channel Flip Prob", "Context Length", "Markov Transition Probabilities","No. of Errors", "No of changes by DUDE", "Number of right changes", "fraction of changes", "fraction of right changes", "Ratio"] 
        RowstoWrite =  [ Heading ]  
        RowstoWrite += [[ self.Input.SequenceLength, self.p, self.ContextLength, float("{0:.2f}".format(self.r1)) , sum(z1), sum(z3), self.Output.CorrectedByContext,  fractionOfChanges, float("{0:.3f}".format( self.Output.CorrectedByContext/float( sum( z1 ) +1 ) ) ), self.IIDMarkovRatio ]]
         
        try:
            # copying data from the exiting file
            with open(Filename, 'r') as f:
                reader = csv.reader(f) # pass the file to our csv reader
                for row in reader:     # iterate over the rows in the file
                    if ( len(row) == 0 or row[0] == "InputSequence Length" ):
                        continue
                    RowstoWrite.append(row)
        except:
            print( "Creating Result.csv")
        #f.close()
        #Writing all the data
        with open( Filename, 'w') as f:                                    
            writer = csv.writer(f)                                                       
            writer.writerows(RowstoWrite)
        f.close()
        
    def TransitionDic(self, markovTransitionProbab ):
        self.r1 = markovTransitionProbab
        r2 = (1 - self.r1)/3
        r1 = self.r1
        self.MarkovTransitionDictionary = OrderedDict( { 'A' : OrderedDict( {'A':r1, 'G':r2, 'T':r2, 'C':r2} ),
                                              'G' : OrderedDict( {'A':r2, 'G':r1, 'T':r2, 'C':r2} ),
                                              'T' : OrderedDict( {'A':r2, 'G':r2, 'T':r1, 'C':r2} ),
                                            'C' : OrderedDict( {'A':r2, 'G':r2, 'T':r2, 'C':r1} )
                                            } )
        
    def Markov(self):
        #Looping Over Markov Transition Probabilities
        for markovTransitionProbab in numpy.arange(0.05,1,.05):
            self.TransitionDic(markovTransitionProbab)
            self.Input = MarkovModelSequence( self.Alphabet, self.SequenceLength, self.MarkovTransitionDictionary, self.ChainWeight)
            # Creating the channel class
            Channel = DiscreteMemoryChannel( self.Input, self.TransitionDictionary )

            for i in range( self.ContextLengthMin, self.ContextLengthMax ):
                self.NumberOfInstances += 1 
                self.ContextLength = i
                # Creating the output class
                self.Output = DUDEOutputSequence( Channel, self.LossFunction, self.Input, ContextLength = self.ContextLength, shouldIprint = self.shouldIprint)
                #Decoding the Sequence
                self.PrintInformation(Filename="Results_test.csv")

    def DependenceonLength(self):
        for length in [100,1000,10000,100000]*10+[1000000]*3:
            self.SequenceLength = length
            for markovTransitionProbab in numpy.arange(0.7,1,.05):
                self.TransitionDic(markovTransitionProbab)
                self.Input = MarkovModelSequence( self.Alphabet, self.SequenceLength, self.MarkovTransitionDictionary, self.ChainWeight)
                # Creating the channel class
                Channel = DiscreteMemoryChannel( self.Input, self.TransitionDictionary )
    
                for i in range( self.ContextLengthMin, self.ContextLengthMax ):
                    self.NumberOfInstances += 1 
                    self.ContextLength = i
                    # Creating the output class
                    self.Output = DUDEOutputSequence( Channel, self.LossFunction, self.Input, ContextLength = self.ContextLength, shouldIprint = self.shouldIprint)
                    self.PrintInformation(Filename="Results_length.csv")

    def mainRealData(self, filename, printResultFile):
        self.r1 = -1 #Bad code
        #Calling the functions

        self.Input = ReadInputFromFile(filename)
        # Creating the channel class
        Channel = DiscreteMemoryChannel( self.Input, self.TransitionDictionary )

        for i in range( self.ContextLengthMin, self.ContextLengthMax ):
            self.NumberOfInstances += 1 
            self.ContextLength = i
            # Creating the output class
            self.Output = DUDEOutputSequence( Channel, self.LossFunction, self.Input, ContextLength = self.ContextLength, shouldIprint = self.shouldIprint)
            groupContexts( self.Output.HashDictionary, self.Output.Alphabet)
            self.PrintInformation(printResultFile)
            self.GroupInfo = groupContexts( self.Output.HashDictionary, self.Output.Alphabet)
            AnalyzeContextGroupInfo( self.GroupInfo )
    
    def ReadData(self, filename, NoOfReads, printResultFile = "Results_Read_"+os.name+".csv"):
        self.r1 = -1 #Bad code
        #Calling the functions

        self.Input = ReadFromReads(filename, NoOfReads)
        # Creating the channel class
        Channel = DiscreteMemoryChannel( self.Input, self.TransitionDictionary )

        for i in range( self.ContextLengthMin, self.ContextLengthMax ):
            self.NumberOfInstances += 1 
            self.ContextLength = i
            # Creating the output class
            self.Output = DUDEOutputSequence( Channel, self.LossFunction, self.Input, ContextLength = self.ContextLength, shouldIprint = self.shouldIprint)
            self.GroupInfo = groupContexts( self.Output.HashDictionary, self.Output.Alphabet)
            AnalyzeContextGroupInfo( self.GroupInfo)
            self.PrintInformation(printResultFile)
    
    def SimpleMain(self, markovTransitionProbab):
        self.NumberOfInstances = 0
        #Calling the functions
        self.TransitionDic(markovTransitionProbab)
        self.Input = MarkovModelSequence( self.Alphabet, self.SequenceLength, self.MarkovTransitionDictionary, self.ChainWeight)
        # Creating the channel class
        Channel = DiscreteMemoryChannel( self.Input, self.TransitionDictionary )
        # Creating the output class
        self.Output = DUDEOutputSequence( Channel, self.LossFunction, self.Input, ContextLength = self.ContextLength, shouldIprint = self.shouldIprint)
        self.PrintInformation(Filename="Del.csv")


    def IIDMarkov(self, markovTransitionProbab):
        self.TransitionDic(markovTransitionProbab)
#
        for ratio in numpy.arange(.4,1.01,.025):
            self.IIDMarkovRatio = ratio
            self.Input = IIDandMarkovSequence( self.Alphabet, ratio, self.SequenceLength, self.MarkovTransitionDictionary )
            # Creating the channel class
            Channel = DiscreteMemoryChannel( self.Input, self.TransitionDictionary )
         
            for CL in range(self.ContextLengthMin, self.ContextLengthMax):
                self.ContextLength = CL       # Creating the output class
                print( "\n\nRATIO === ", ratio, "Context Length", CL, "Length", self.SequenceLength )
                self.Output = DUDEOutputSequence( Channel, self.LossFunction, self.Input, ContextLength = self.ContextLength, shouldIprint = self.shouldIprint)
                self.PrintInformation(Filename="ZIIDMarkovResults_"+os.name+".csv")

    def ReadSimulation(self, filename, ReadLength = 100,   outputfile = "Results_reads_simulation__"+os.name+".csv"):
        
        #Get the input
        FirstInput = ReadInputFromFile( filename )
        #Get Reads and combine the reads
        CoverageDepth = 10
        self.Input = ReadsInput( FirstInput, ReadLength, CoverageDepth = CoverageDepth)
        Channel = DiscreteMemoryChannel( self.Input, self.TransitionDictionary )
        for CL in range(self.ContextLengthMin, self.ContextLengthMax):
            self.ContextLength = CL       # Creating the output class
            print( "Context Length", CL, "Length", self.SequenceLength )
            self.Output = DUDEOutputSequence( Channel, self.LossFunction, self.Input, ContextLength = self.ContextLength, shouldIprint = self.shouldIprint)
            self.PrintInformation( Filename=outputfile )