'''
Created on 2020/05/05

@author: ukai
'''
from framework import BuildOrder
import json

class ConcBuildOrder(BuildOrder):
    '''
    classdocs
    '''


    def __init__(self, nIteration, nSeq, nHorizonValueOptimization, nIntervalPolicyOptimization, nBatchPolicyOptimization, nSaveInterval, description, nLevers):
        '''
        Constructor
        '''
        
        super(ConcBuildOrder, self).__init__(nIteration, nSeq, nHorizonValueOptimization, nIntervalPolicyOptimization, nBatchPolicyOptimization, nSaveInterval, description)
        
        self.nLevers = nLevers
        
    def getnLevers(self): 
        return self.nLevers
        
    def toDict(self):
        
        return dict(
            nIteration=self.nIteration,
            nSeq=self.nSeq,
            nHorizonValueOptimization=self.nHorizonValueOptimization,
            nIntervalPolicyOptimization=self.nIntervalPolicyOptimization,
            nBatchPolicyOptimization=self.nBatchPolicyOptimization,
            nSaveInterval=self.nSaveInterval,
            description=self.description,
            nLevers=self.nLevers,
            )