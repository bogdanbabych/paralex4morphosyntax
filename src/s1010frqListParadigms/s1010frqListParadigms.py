'''
Created on 15 Apr 2019

@author: bogdan
'''

import os, sys, re
import mdParadigms2
from collections import defaultdict
from builtins import int




class clFrqListParadigms(object):
    '''
    open frequency dictionary; read into memory, load Paradigms class
    
    '''


    def __init__(self, FFrqList):
        '''
        Constructor
        '''
        sys.stderr.write('initialising \n')
        self.DFrqList = {}
        sys.stderr.write(str(sys.getsizeof(self.DFrqList)) + '\n')
        self.frqListReader(FFrqList)
        sys.stderr.write(str(sys.getsizeof(self.DFrqList)) + '\n')
        
        OParadigms = mdParadigms2.clParadigms('mdParadigms2.txt')
        self.DInfl = OParadigms.getInfl() # dictionary of inflections 
        self.DClass = OParadigms.getClass() # dictionary of classes
        self.DHypotheses = defaultdict(int)

        return


    def frqListReader(self, FFrqList):
        for SLine in FFrqList:
            SLine = SLine.strip()
            try:
                (SFrq, SWord) = re.split(' ', SLine, 1)
            except:
                continue
            
            if int(SFrq) > 3:
                self.DFrqList[SWord] = int(SFrq)
            
        
        
        return
    
    
    def printData(self):
        sys.stderr.write('checking hypotheses \n\n')
        IConfirmed = 0
        
        
        for (k, v) in sorted(self.DFrqList.items(), key=lambda x: x[1], reverse=True) :
            # find the top confirmed hypothesis
            DLocHypotheses = {} # ranked local hypotheses: which one gets more matches
            if v > 1:
                # sys.stdout.write(k + '\t' + str(v) + '\n')
                LSplits = self.splitByInfl(k, self.DInfl)
                for TSplit in LSplits:
                    (SStem, SInfl, LClassNCateg) = TSplit
                    for (SClass, Categs, Example) in LClassNCateg:
                        ICountHypothesis = 0
                        # BConfirmHypothesis = False
                        LHypotheses = self.genByInfl(SStem, SClass)
                        LHypotheses2 = []
                        for (SWordForm, SCat, SExamp) in LHypotheses:
                            if SWordForm in self.DFrqList.keys():
                                THyp2 = (SWordForm, SCat, SExamp, 'FOUND')
                                ICountHypothesis += 1
                                # + record 'found' or 'generated' --- to be able to count found items...
                            else:
                                THyp2 = (SWordForm, SCat, SExamp, '-proj')
                                # pass
                            LHypotheses2.append(THyp2)
                        if ICountHypothesis > 4:
                            IConfirmed += 1
                            if IConfirmed % 50000 == 0: sys.stderr.write(str(IConfirmed) + ' : ' + str(THyp2) + '\n')
                            # BConfirmHypothesis = True
                            # SetHyp = frozenset(LHypotheses)
                            SetHyp = frozenset(LHypotheses2)
                            self.DHypotheses[SetHyp] += 1
                            # sys.stdout.write(str(LHypotheses) + '\n\n')
                            # record in a dictionary and print separately...

        return
    
    
    def printHypotheses(self):
        sys.stderr.write('writing paradigms...\n')
        j = 0
        # sys.stdout.write(str(sorted(self.DHypotheses.items(), reverse = False)) + '\n\n')

        for (k, v) in sorted(self.DHypotheses.items(), key=lambda x: x[1], reverse = True):
        # for (k, v) in sorted(self.DHypotheses.items(), reverse = False):
            j+=1;
            if j% 50000 == 0: sys.stderr.write(str(k) + '\n')
            sys.stdout.write(str(sorted(k)) + '\n\n')
            LKeys = list(k)
            LKeysSorted = sorted(LKeys, key=lambda y: y[1])
            TLemma = LKeysSorted[0]
            SLemma = TLemma[0]
            SFrq = str(v)
            for el in sorted(LKeys, key=lambda y: y[1]):
                (SWordForm, SPos, SPattern, SFound) = el
                # sys.stdout.write(str(el) + '\t' + str(v) + '\n')
                sys.stdout.write('%(SWordForm)s %(SLemma)s %(SPos)s %(SPattern)s %(SFound)s %(SFrq)s\n' % locals())
            sys.stdout.write('\n')
            
                
    

    
    def splitByInfl(self, SWord, DInfl):
        '''
        returns splits by inflection (empty inflection not used now)
        split word; then form hypotheses by inflection class...
        '''
        LSplits = []
        for SKey, LValue in DInfl.items():
            if SKey == '': continue
            m = re.search('^(.+?)(' + SKey + ')$', SWord)
            if m == None: continue
            TMGroups = m.groups() # match groups
            TGroups = (TMGroups[0], TMGroups[1], LValue)
            
            # TGroups = TGroups + tuple(SValue)
            LSplits.append(TGroups)
        # the list of tuples returned
        # sys.stderr.write(str(LSplits) + '\n')
        return LSplits
    
    def genByInfl(self, SStem, SClass):
        
        LTHypotheses = []
        
        LTInflectCategs = self.DClass[SClass]
        for (SInfl, SCats, SExamp) in LTInflectCategs:
            THypoth = (SStem + SInfl, SCats, SExamp)
            LTHypotheses.append(THypoth)
        
        
        return LTHypotheses






if __name__ == '__main__':
    '''
    the first argument should be a frequency glossary of word forms in the format generated from corpus by shell commands:
    
    
    '''
    # SFDebug = open(sys.argv[2] + '_debug.txt', 'w')
    FFrqList = open(sys.argv[1], 'rU')
    
    OFrqListParadigms = clFrqListParadigms(FFrqList)
    OFrqListParadigms.printData()
    OFrqListParadigms.printHypotheses()