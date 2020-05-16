'''
Created on 2020/05/05

@author: ukai
'''
from framework import BuildOrder

class ConcBuildOrder(BuildOrder):
    '''
    classdocs
    '''


    def __init__(self, nIteration, nSeq, nHorizonValueOptimization, nIntervalPolicyOptimization, nBatchPolicyOptimization, nSaveInterval, description, tConstant, nHiddenValueApproximator):
        '''
        Constructor
        '''
        
        super(ConcBuildOrder, self).__init__(nIteration, nSeq, nHorizonValueOptimization, nIntervalPolicyOptimization, nBatchPolicyOptimization, nSaveInterval, description)
        
        self.tConstant = tConstant
        self.nHiddenValueApproximator = nHiddenValueApproximator
                
    def toDict(self):
        
        return dict(
            nIteration=self.nIteration,
            nSeq=self.nSeq,
            nHorizonValueOptimization=self.nHorizonValueOptimization,
            nIntervalPolicyOptimization=self.nIntervalPolicyOptimization,
            nBatchPolicyOptimization=self.nBatchPolicyOptimization,
            nSaveInterval=self.nSaveInterval,
            description=self.description,
            tConstant=self.tConstant,
            nHiddenValueApproximator = self.nHiddenValueApproximator,
            )