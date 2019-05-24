'''
Created on 17 Sep 2014

@author: bogdan
'''

import sys, os, re
from collections import defaultdict


class procGram(object):
    '''
    purpose of the class:
        create a frequency list of word forms
        match word forms to paradigms -- including frequency analysis...
        take into account contextual information
    '''


    def __init__(self, SFileName):
        '''
        opening files, calling procedures...
        '''
        self.DWordFreq = defaultdict(int)
        FInText = open(SFileName, 'rU')
        for SLine in FInText:
            SLine = SLine.rstrip()
            LWords = self.tokenize(SLine)
            for SWord in LWords:
                self.DWordFreq[SWord] += 1
                
        self.printSorted(self.DWordFreq)
        
            
            
    def tokenize(self, SLine):
        LWords = re.split('[ ,\.\;\:\-\(\)\[\]\!\?\/\*\"0-9\#\%\_]+', SLine)
        return LWords
    
    
    def printSorted(self, D2Print):
        for Key, Value in sorted(D2Print.items()):
            print(str(Key) + '\t' + str(Value))
            
    
    

if __name__ == '__main__':
    ProcGram = procGram(sys.argv[1])