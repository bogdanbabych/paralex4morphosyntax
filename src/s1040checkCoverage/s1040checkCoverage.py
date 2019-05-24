#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 26 Apr 2019

@author: bogdan
'''

import os, sys, re
from collections import defaultdict
# todo: figures for corpus coverage = add frequencies of non-covered words...


class clCheckCoverage(object):
    '''
    comparing two frq dicts - how much lexicon is different, frq ranges reporting
    '''


    def __init__(self, FInput01d, FInput02, IFrqThreshold, f, LFPar, SFInput02):
        '''
        Constructor
        '''
        
        # to be able to run processes in parallel, all use different added paradigms for testing
        try:
            Arg4 = LFPar[0]
            path, file = os.path.split(Arg4)
            Fs1040checkCoverage = open('s1040checkCoverage-' + file + '.csv', 'a')
        except:
            Arg4 = ''
            file = ''
            Fs1040checkCoverage = open('s1040checkCoverage.csv', 'a')
        
        pf, e = os.path.splitext(SFInput02)
        
        # to prevent overwriting
        SFOutput1 = pf + str(IFrqThreshold) + file + '-out1.txt'
        SFOutput2 = pf + str(IFrqThreshold) + file + '-out2.txt'
        SFOutput2ok = pf + str(IFrqThreshold) + file + '-out2ok.txt'
        SFOutput3 = pf + str(IFrqThreshold) + file + '-out3par.txt'
        
        FOutput1 = open(SFOutput1, 'w')
        FOutput2 = open(SFOutput2, 'w')
        FOutput2ok = open(SFOutput2ok, 'w')
        FOutput3 = open(SFOutput3, 'w')
        
        
        
        self.IFrqThresholdGlob = IFrqThreshold
        
        self.ICorpusLength = 0
        self.ICorpusTypes = 0

        self.DFrq01d = defaultdict(int)
        self.DFrq02 = defaultdict(int)
        
        self.readParadigms(FInput01d, self.DFrq01d)
        self.readFrqDict(FInput02, self.DFrq02)
        
        # added paradigms
        self.DFrq03dPar = defaultdict(int)
        for SFPar in LFPar:
            FPar = open(SFPar, 'rU', encoding='utf-8', errors='ignore')
            self.readParadigms(FPar, self.DFrq03dPar)
            
        
        
        
        # DDiffFrq = self.compDicts(self.DFrq01, self.DFrq02)
        # DDiffFrq, ITypesNotCovered, ITokensNotCovered = self.compDicts(self.DFrq02, self.DFrq01d, self.DFrq03dPar)
        DDiffFrq, ITypesNotCovered, ITokensNotCovered, DDiffFrq2, ITypesNotCovered2, ITokensNotCovered2, DDiffFrq2ok, ITypesCovered2, ITokensCovered2, DDiffFrq3Par, ITypesNotCovered3Par, ITokensNotCovered3Par = self.compDicts(self.DFrq02, self.DFrq01d, self.DFrq03dPar)
        
        # self.printFrqDict(self.DFrq01)
        # self.printFrqDict(self.DFrq02)
        
        FPCNotCoveredTypes = ITypesNotCovered / float(self.ICorpusTypes)
        FPCNotCoveredTokens = ITokensNotCovered / float(self.ICorpusLength)
        
        FPCNotCoveredTypes2 = ITypesNotCovered2 / float(self.ICorpusTypes)
        FPCNotCoveredTokens2 = ITokensNotCovered2 / float(self.ICorpusLength)

        FPCCoveredTypes2 = ITypesCovered2 / float(self.ICorpusTypes)
        FPCCoveredTokens2 = ITokensCovered2 / float(self.ICorpusLength)

        FPCNotCoveredTypes3Par = ITypesNotCovered3Par / float(self.ICorpusTypes)
        FPCNotCoveredTokens3Par = ITokensNotCovered3Par / float(self.ICorpusLength)
        

        sys.stdout.write('# %(ITypesNotCovered)d types not covered; \n# %(ITokensNotCovered)d tokens not covered \n' % locals())
        sys.stdout.write('# %(FPCNotCoveredTypes).5f pc types not covered; \n# %(FPCNotCoveredTokens).5f pc tokens not covered \n' % locals())

        sys.stdout.write('# \n# %(ITypesNotCovered2)d types2 not covered with added Paradigms; \n# %(ITokensNotCovered2)d tokens2 not covered with added Paradigms; \n' % locals())
        sys.stdout.write('# %(FPCNotCoveredTypes2).5f pc types not covered w added Paradigms; \n# %(FPCNotCoveredTokens2).5f pc tokens not covered w added Paradigms\n' % locals())

        sys.stdout.write('# \n# %(ITypesCovered2)d types covered! = Par contribution; \n# %(ITokensCovered2)d tokens covered! = Par contribution\n' % locals())
        sys.stdout.write('# %(FPCCoveredTypes2).5f pc types covered!; = Par contribution \n# %(FPCCoveredTokens2).5f pc tokens covered! = Par contribution\n' % locals())

        sys.stdout.write('# \n# %(ITypesNotCovered3Par)d types not covered with Par only; \n# %(ITokensNotCovered3Par)d tokens not covered with Par only\n' % locals())
        sys.stdout.write('# %(FPCNotCoveredTypes3Par).5f pc types not covered with Par only; \n# %(FPCNotCoveredTokens3Par).5f pc tokens not covered with Par only\n' % locals())


        sys.stdout.write('# ' + str(self.ICorpusLength) + ' corpus length (tokens) \n')
        sys.stdout.write('# ' + str(self.ICorpusTypes) + ' corpus diversity (types) \n')
        self.FlTypeTokenRatio = self.ICorpusTypes / float(self.ICorpusLength)
        sys.stdout.write('# ' + str(self.FlTypeTokenRatio) + ' type/token ratio \n#\n#\n')
        
        ICorpusLengthLoc = self.ICorpusLength
        ICorpusTypesLoc = self.ICorpusTypes
        FlTypeTokenRatioLoc = self.FlTypeTokenRatio
        
        # Fs1040checkCoverage.write('%(f)s,%(IFrqThreshold)d,%(ITypesNotCovered)d,%(ITokensNotCovered)d,%(FPCNotCoveredTypes).5f,%(FPCNotCoveredTokens).5f,%(ICorpusLengthLoc)d,%(ICorpusTypesLoc)d,%(FlTypeTokenRatioLoc).5f\n' % locals())
        Fs1040checkCoverage.write('%(f)s,%(IFrqThreshold)d,%(ITypesNotCovered)d,%(ITokensNotCovered)d,%(FPCNotCoveredTypes).5f,%(FPCNotCoveredTokens).5f,%(ICorpusLengthLoc)d,%(ICorpusTypesLoc)d,%(FlTypeTokenRatioLoc).5f,%(ITypesNotCovered2)d,%(ITokensNotCovered2)d,%(FPCNotCoveredTypes2).5f,%(FPCNotCoveredTokens2).5f,%(ITypesCovered2)d,%(ITokensCovered2)d,%(FPCCoveredTypes2).5f,%(FPCCoveredTokens2).5f,%(ITypesNotCovered3Par)d,%(ITokensNotCovered3Par)d,%(FPCNotCoveredTypes3Par).5f,%(FPCNotCoveredTokens3Par).5f\n' % locals())

        self.printFrqDict(DDiffFrq, FOutput1)
        self.printFrqDict(DDiffFrq2, FOutput2)
        self.printFrqDict(DDiffFrq2ok, FOutput2ok)
        self.printFrqDict(DDiffFrq3Par, FOutput3)
 
        
        return
        
    # Par dictionary = added paradigms
    def compDicts(self, DFrq01, DFrq02, DFrq03Par):
        if len(DFrq03Par.items()) > 0:
            BCheckPars = True
        else:
            BCheckPars = False
        
        DDiffFrq = {}
        DDiffFrq2 = {} # differences = not found in any dictionary
        DDiffFrq2ok = {} # not found in static, but found in dynamic paradigms!
        DDiffFrq3Par = {}
        ITokensNotCovered = 0
        ITypesNotCovered = 0

        ITokensCovered2 = 0
        ITypesCovered2 = 0

        ITokensNotCovered2 = 0
        ITypesNotCovered2 = 0

        
        ITypesNotCovered3Par = 0
        ITokensNotCovered3Par = 0

        sys.stderr.write('checking coverage\n')
        j = 0
        for (k, v) in sorted(DFrq01.items(), key=lambda x: x[1], reverse = True):
            j +=1
            if j % 100000 == 0: sys.stderr.write(str(j) + '\n')
            
            if k not in DFrq02.keys():
                DDiffFrq[k] = v
                ITypesNotCovered += 1
                ITokensNotCovered += v
                
                # assessing effects of the added paradigms
                if BCheckPars:
                    if k in DFrq03Par.keys():
                        DDiffFrq2ok[k] = v
                        ITypesCovered2 +=1
                        ITokensCovered2 += v
                    else:
                        DDiffFrq2[k] = v
                        ITypesNotCovered2 += 1
                        ITokensNotCovered2 += v
                
                
            if k not in DFrq03Par.keys():
                DDiffFrq3Par[k] = v
                ITypesNotCovered3Par += 1
                ITokensNotCovered3Par += v

                
            
            # sys.stdout.write(str(v) + ' ' + str(k) + '\n')
            
        
        
        return DDiffFrq, ITypesNotCovered, ITokensNotCovered, DDiffFrq2, ITypesNotCovered2, ITokensNotCovered2, DDiffFrq2ok, ITypesCovered2, ITokensCovered2, DDiffFrq3Par, ITypesNotCovered3Par, ITokensNotCovered3Par
    
    

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
    SFInput01 = sys.argv[1]
    SFInput02 = sys.argv[2]
    SFrqThreshold = sys.argv[3]
    IFrqThreshold = int(SFrqThreshold)
    
    # add paradigm updates, collect everything from sys.argv[4] onwards
    LFInput03par = []
    
    try:
        LFPar = sys.argv[4:]
    except:
        LFPar = []
        

    # FInput = open(SFInput, 'rU')
    FInput01d = open(SFInput01, 'rU', encoding='utf-8', errors='ignore')
    FInput02 = open(SFInput02, 'rU', encoding='utf-8', errors='ignore')
    
    
    p,f = os.path.split(SFInput02)
    
    
    
    sys.stderr.write('\n comparing: %(SFInput01)s %(SFInput02)s %(f)s \n' % locals())
    
    
    
    # dictionary and frqlist (corpus)
    OCheckCoverage = clCheckCoverage(FInput01d, FInput02, IFrqThreshold, f, LFPar, SFInput02)
    
    
    
    