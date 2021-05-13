from BitHash import BitHash
from BitVector import BitVector
import math 

class BloomFilter(object): 
    #This will calculate the number if bits needed
    #it will store numKeys, using numHashes and hashFunctions and will
    #have a specific false positive rate
    def __bitsNeeded(self, numKeys, numHashes, maxFalsePositive):
        
        # Equation B
        #Get phi from the maxFalsePositive and the number of hashes
        phi = (1 - (maxFalsePositive ** (1/numHashes)))
        
        #Get N from the number of hashes, phi and number of keys
        N = numHashes / (1 - (phi ** (1/numKeys)))
        
        #Return N rounded (it returns a float so needs to be rounded to an int)
        return round(N)    
    
    # Create a Bloom Filter that will store numKeys keys, using 
    # numHashes hash functions, and that will have a false positive 
    # rate of maxFalsePositive.
    # All attributes must be private.
    def __init__(self, numKeys, numHashes, maxFalsePositive):
        
        #Create an attribute for numKeys, numHashes and maxFalsePos
        self.__numKeys = numKeys
        self.__numHashes = numHashes
        self.__maxFalsePositive = maxFalsePositive
        
        #Set the number of bits we have set to 0
        #We are starting out with no bits set
        self.__bitsSet = 0 
        
        #This will calculate how many bits we need
        #Using the bitsNeeded from above
        self.__bits = self.__bitsNeeded(numKeys, numHashes, maxFalsePositive)
        
        #Then create a bitVector with the number of bits that we 
        #just calculated above
        self.__b = BitVector(size = self.__bits)
    
    # insert the specified key into the Bloom Filter.
    def insert(self, key):
        #Create an empty list to keep track of just hashed numbers
        #The list will have the hashed numbers
        #Not the numbers % bits
        hashed = []
        
        #Start by hashing the first key 
        hashed += [BitHash(key, 0)] 
        
        #Then starting at 1, loop for the number of hashes we want
        #The number of hashes is specified by the client
        for i in range (1, self.__numHashes):
            
            #Then add those hashes to the list
            #Each time you hash you use the previous  hashed number
            hashed += [BitHash(key, hashed[i-1])]
            
        #now loop through the list
        for element in hashed:
            
            #Now take that element and % it by the number of bits
            #To get the actual index the key should be in the bitVector
            
            #If that index in the bitVector is not 1
            if self.__b[element % self.__bits] != 1:
                #Increase the number of bits set by 1
            #Needed the above code because otherwise
            #Even when we are not setting a new bit to 1 (it was already 1)
            #It will increase bits set
                self.__bitsSet += 1
                
            #Either way set that index to 1
            #Doesn't matter whether the bit was already 1, set it to 1 anyway
            self.__b[element % self.__bits] = 1

    
    # Returns True if key MAY have been inserted into the Bloom filter. 
    # Returns False if key definitely hasn't been inserted into the BF.
    # See the "Bloom Filter details" slide for how find works.
    def find(self, key):
        #Create an empty list to store the hash numbers not % yet
        hashed = []
        
        #Add the first hashed number to the list
        hashed += [BitHash(key, 0)]
        
        #Loop from 1 to the number of hashes
        #From 1 since we have already used 0
        for i in range (1, self.__numHashes):
            
            #Add to the list the hashed numbers using the hashed number
            #from before (that was stored in the list)
            hashed += [BitHash(key, hashed[i-1])]
            
        #loop through the elements in the list
        for element in hashed:
            
            #If that index in the bitVector is 0
            if self.__b[element % self.__bits] == 0:
                
                #return False
                #It can't possibly be that the key was inserted
                return False
            
        #Otherwise return true
        #The key most probably was inserted
        return True
    
    def falsePositiveRate(self):
        #solve for phi which is the actual current proportion
        #Of bits in the bit vector that are still 0
        #Find this by subtracting the bits set from the number
        #Of bits in the whole bitVector and divide by the number of bits
        #That gives you proportion of bits that are 0 still
        phi = (self.__bits - self.__bitsSet)/ self.__bits
        
        #Then using the equation get the projected current false positive rate
        #This is based on the number of bits that are actually set in the 
        #bloom filter
        P = (1 - phi) ** self.__numHashes
        return P
       
    # Returns the current number of bits ACTUALLY set in this Bloom Filter
    def numBitsSet(self):
        
        #Created an attribute above... this returns the attribute
        return self.__bitsSet
       

def __main():
    numKeys = 100000
    numHashes = 4
    maxFalse = .05
    
    # create the Bloom Filter
    f = BloomFilter(numKeys, numHashes, maxFalse)
    
    # Open the file 
    fin = open("wordlist.txt")
    
    #Read the first numKeys words from the file and insert them
    #into the bloom filter
    for i in range (numKeys):
        word = fin.readline()
        f.insert(word)
    
    #Close the file 
    fin.close()

    # Print out what the PROJECTED false positive rate should 
    print("Projected false positive rate: ", f.falsePositiveRate())
    # THEORETICALLY be based on the number of bits that ACTUALLY ended up being set
    # in the Bloom Filter

    #reopen the file
    fin = open("wordlist.txt")
    
    #Set missing to 0
    #this will count how many words that were inserted are missing 
    #From the bloom filter
    missing = 0
    
    #Loop numKeys times
    for i in range (numKeys):
        
        #Read a word from the text
        word = fin.readline()
        
        #Try find the word in the blooom Filter. If it returns false
        if f.find(word) == False:
            
            #Add one to missing
            missing += 1
    
    print(missing, "keys are missing!")
    
    #Keep track of the words that are found in the bloomFilter
    #even though they shouldn't have been
    falseFound = 0
    
    #Loop numKeys times
    for i in range (numKeys):
        #Read the line
        #These are words that were not inserted
        word = fin.readline()
        
        #If the word is found in the bloom filter
        if f.find(word) == True:
            
                #Add one to falsely found.
                #The word was not inserted! 
                falseFound += 1
    #This is the proportion of false positives that were encountered
    #Divide the falseFound by the number of Keys we checked
    falsePositiveRate = falseFound/numKeys
    
    #And print out the result
    print("Actual false pos rate: ", falsePositiveRate)

    
if __name__ == '__main__':
    __main()       
