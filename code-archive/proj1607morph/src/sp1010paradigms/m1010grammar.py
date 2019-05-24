'''
Created on 26 Oct 2014

@author: bogdan
'''


import sys, os, re
from collections import defaultdict
import mdParadigms
# from s1010paradigms.mdParadigms import clParadigms
FDebug = open('m1010grammar-debug.txt', 'w')


class procGrammar(object):
	'''
	class : extracting grammar from a frequency list
	'''


	def __init__(self, SFileName):
		'''
		openning files, etc.
		'''
		OParadigms = mdParadigms.clParadigms('uaparadigms.txt')
		self.DInfl = OParadigms.getInfl()
		DClass = OParadigms.getClass()
		
		self.DWordFreq = defaultdict(int)
		FInText = open(SFileName, 'rU')
		for SLine in FInText:
			SLine = SLine.rstrip()
			if re.match('<', SLine): continue
			if re.search('[ ,\.\;\:\-\(\)\[\]\!\?\/\*\"0-9\#\%\_\*\=\+]+', SLine): continue # Ukrainian assumed 
			LLine = SLine.split('\t')
			(SWord, SLemma, SPoS) = LLine[:3]
			self.DWordFreq[SWord] += 1
		
		self.printDict(self.DInfl)
		self.printDict(DClass)
		# self.printDictSK(self.DWordFreq)	
		self.printDictSplit(self.DWordFreq)
		
		return
	
	
	def splitByInfl(self, SWord, DInfl):
		LSplits = []
		for SKey, SValue in DInfl.items():
			if SKey == '': continue
			m = re.search('^(.+?)(' + SKey + ')$', SWord)
			if m == None: continue
			TGroups = m.groups()
			TGroups = TGroups + tuple(SValue)
			LSplits.append(TGroups)
		return LSplits
	
	
	def printDict(self, D2Print):
		for Key, Value in sorted(D2Print.items(), key=lambda a:a[1], reverse=False):
			# print(str(Key) + '\t' + str(Value))
			FDebug.write(str(Key) + '\t' + str(Value) + '\n')

	def printDictSK(self, D2Print):
		for Key, Value in sorted(D2Print.items(), key=lambda a:a[0], reverse=False):
			# print(str(Key) + '\t' + str(Value))
			FDebug.write(str(Key) + '\t' + str(Value) + '\n')
	def printDictSplit(self, D2Print):
		for Key, Value in sorted(D2Print.items(), key=lambda a:a[0], reverse=False):
			# print(str(Key) + '\t' + str(Value))
			LWordSplits = self.splitByInfl(Key, self.DInfl)
			FDebug.write(str(Key) + '\t' + str(LWordSplits) + '\t' + str(Value) + '\n')
			
		return
	
			
		




if __name__ == '__main__':
	procGrammar(sys.argv[1])
			