'''
Created on 26 Apr 2019

@author: bogdan
'''

import os, sys, re
from collections import defaultdict



class clCompareFrqDicts(object):
    '''
    comparing two frq dicts - how much lexicon is different, frq ranges reporting
    '''


    def __init__(self, FInput01, FInput02):
        '''
        Constructor
        '''
        self.DFrq01 = defaultdict(int)
        self.DFrq02 = defaultdict(int)
        
        self.readFrqDict(FInput01, self.DFrq01)
        self.readFrqDict(FInput02, self.DFrq02)
        
        # DDiffFrq = self.compDicts(self.DFrq01, self.DFrq02)
        DDiffFrq = self.compDicts(self.DFrq02, self.DFrq01)

        
        # self.printFrqDict(self.DFrq01)
        # self.printFrqDict(self.DFrq02)
 
        self.printFrqDict(DDiffFrq)
 
        
        return
        
        
    def compDicts(self, DFrq01, DFrq02):
        DDiffFrq = {}
        sys.stderr.write('printing frq\n')
        j = 0
        for (k, v) in sorted(DFrq01.items(), key=lambda x: x[1], reverse = True):
            j +=1
            if j % 100000 == 0: sys.stderr.write(str(j) + '\n')
            
            if k not in DFrq02.keys():
                DDiffFrq[k] = v
            
            # sys.stdout.write(str(v) + ' ' + str(k) + '\n')
            
        
        
        return DDiffFrq
    
        
    def readFrqDict(self, FInput, DFrq):
        
        sys.stderr.write('reading dictionary\n')
        i = 0
        
        # with codecs.open(file_name, 'r', encoding='utf-8', errors='ignore') as fdata:
        for SLine in FInput:
            i += 1
            ICountWords = 0
            if i %100000 == 0: sys.stderr.write(str(i) + '\n')
            SLine = SLine.strip()
            try:
                LLine = re.split('[ \t]+', SLine)
                WForm = LLine[1]
                SFrq = LLine[0]
                IFrq = int(SFrq)
                ICountWords += 1
                DFrq[WForm] = IFrq

            except:
                continue
            
            # DFrq[WForm] += 1

        
        return
    
    def printFrqDict(self, DFrq):
        sys.stderr.write('printing frq\n')
        j = 0
        for (k, v) in sorted(DFrq.items(), key=lambda x: x[1], reverse = True):
            j +=1
            if j % 100000 == 0: sys.stderr.write(str(j) + '\n')
            sys.stdout.write(str(v) + ' ' + str(k) + '\n')
            
        
        return
        
        
if __name__ == '__main__':
    SFInput01 = sys.argv[1]
    SFInput02 = sys.argv[2]

    # FInput = open(SFInput, 'rU')
    FInput01 = open(SFInput01, 'rU', encoding='utf-8', errors='ignore')
    FInput02 = open(SFInput02, 'rU', encoding='utf-8', errors='ignore')
    OCompareFrqDicts = clCompareFrqDicts(FInput01, FInput02)
    