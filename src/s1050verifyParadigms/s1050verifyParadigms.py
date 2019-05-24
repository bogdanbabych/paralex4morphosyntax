'''
Created on 2 May 2019

@author: bogdan
'''

import os, sys, re
from collections import defaultdict


class clVerifyParadigms(object):
    '''
    the purpose : select a sample for manual check of paradigm accuracy...
    
    '''


    def __init__(self, FList2Check, FParadigms):
        '''
        Constructor
        '''
        
        self.DFrq = defaultdict(int)
        self.readFrqDict(FList2Check, self.DFrq)
        
        
        self.DWForm2LemFeat = defaultdict(list)
        self.DLem2Par = defaultdict(list)
        self.DWforms2Par = defaultdict(list)
        
        self.readParadigms(FParadigms, self.DWForm2LemFeat, self.DLem2Par, self.DWforms2Par)



        
        return
    


    def readParadigms(self, FInput, DParadigms):
        
        sys.stderr.write('reading paradigms\n')
        i = 0
        
        # with codecs.open(file_name, 'r', encoding='utf-8', errors='ignore') as fdata:
        for SLine in FInput:
            i += 1
            ICountWords = 0
            if i %100000 == 0: sys.stderr.write(str(i) + '\n')
            SLine = SLine.strip()
            if SLine.startswith('#'): continue
            if SLine == '': continue

            try:
                LLine = re.split('[ \t]+', SLine)
                WForm = LLine[0] # word form is in 0 position, lemma -- in 1st position
                WForm = WForm.lower()
                
                if re.search('[0-9a-z\-\.\,\!\[\]\(\)\*\_\+\%\:\"\'\=\?\|\;ыёъэ]', WForm): continue
                
                # SFrq = LLine[0]
                # IFrq = int(SFrq)
                ICountWords += 1
                DParadigms[WForm] += 1

            except:
                continue
            
            # DFrq[WForm] += 1

        
        return
 

    def readFrqDict(self, FInput, DFrq):
        
        sys.stderr.write('reading dictionary\n')
        i = 0
        
        # with codecs.open(file_name, 'r', encoding='utf-8', errors='ignore') as fdata:
        for SLine in FInput:
            i += 1
            ICountWords = 0
            if i %100000 == 0: sys.stderr.write(str(i) + '\n')
            SLine = SLine.strip()

            if SLine.startswith('#'): continue
            if SLine == '': continue

            try:
                LLine = re.split('[ \t]+', SLine)
                WForm = LLine[1]
                WForm = WForm.lower()
                if re.search('[0-9a-z\-\.\,\!\[\]\(\)\*\_\+\%\:\"\'\=\?\|\;ыёъэ]', WForm): continue
                
                
                SFrq = LLine[0]                
                IFrq = int(SFrq)
                # top limit ; start with 1, not with 0:: frq and higher allowed! = more intuitive ... :: change .sh scripts!!!
                if IFrq < self.IFrqThresholdGlob: continue # comment if want not to ignore hapax legomena ; experiment with this threshold = set for reliable paradigm prediction threshold
        
                
                ICountWords += 1
                DFrq[WForm] += IFrq
                self.ICorpusLength += IFrq
                self.ICorpusTypes += 1 # count number of types (uniq words) in corpus

            except:
                continue
            
            # DFrq[WForm] += 1

        
        return
    
    def printFrqDict(self, DFrq, FOutStream = sys.stdout):
        sys.stderr.write('printing frq\n')
        j = 0
        for (k, v) in sorted(DFrq.items(), key=lambda x: x[1], reverse = True):
            j +=1
            if j % 100000 == 0: sys.stderr.write(str(j) + '\n')
            FOutStream.write(str(v) + ' ' + str(k) + '\n')
            
        
        return
        





        
        
        
if __name__ == '__main__':
    SFList2Check = sys.argv[1]
    SFParadigms = sys.argv[2]
    
    FList2Check = open(SFList2Check, 'rU', encoding='utf-8', errors='ignore')
    FParadigms = open(SFParadigms, 'rU', encoding='utf-8', errors='ignore')
    
    OVerifyParadigms = clVerifyParadigms(FList2Check, FParadigms)
    
    