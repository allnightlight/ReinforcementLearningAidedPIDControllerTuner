'''
Created on 2020/05/26

@author: ukai
'''
from ConcAgent import ConcAgent
from AsmAction import AsmAction

class AsmAgent(ConcAgent):
    '''
    classdocs
    '''

    
    def call(self, observationSequence):
        
        u = self.sampleMvFromPi(observationSequence) # (*, nMv = 1)
        
        return AsmAction(u)