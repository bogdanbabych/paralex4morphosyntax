'''
Created on 25 Apr 2019

@author: bogdan
'''


import os, sys, re
from collections import defaultdict
import codecs

class clConvCorp2Dict(object):
    '''
    corpus to frequency dictionary
    '''


    def __init__(self, FInput):
        '''
        Constructor
        '''
        DFrq = defaultdict(int)
        
        ICountSent = 0
        ICountWords = 0
        
        sys.stderr.write('reading dictionary\n')
        i = 0
        
        # with codecs.open(file_name, 'r', encoding='utf-8', errors='ignore') as fdata:
        for SLine in FInput:
            i += 1
            if i %1000000 == 0: sys.stderr.write(str(i) + '\n')
            SLine = SLine.strip()
            try:
                LLine = re.split('\t', SLine, 2)
                WForm = LLine[0]
                ICountWords += 1
                if LLine[2] == 'SENT': ICountSent +=1
            except:
                continue
            
            DFrq[WForm] += 1
            
        sys.stderr.write('printing frq\n')
        j = 0
        for (k, v) in sorted(DFrq.items(), key=lambda x: x[1], reverse = True):
            j +=1
            if j % 100000 == 0: sys.stderr.write(str(j) + '\n')
            sys.stdout.write(str(v) + ' ' + str(k) + '\n')
            
        
        sys.stderr.write(str(ICountWords) + ' words; ' + str(ICountSent) + ' sentences;\n')
                
        return
    
        
        
        
if __name__ == '__main__':
    SFInput = sys.argv[1]
    # FInput = open(SFInput, 'rU')
    FInput = open(SFInput, 'rU', encoding='utf-8', errors='ignore')
    OConvCorp2Dict = clConvCorp2Dict(FInput)