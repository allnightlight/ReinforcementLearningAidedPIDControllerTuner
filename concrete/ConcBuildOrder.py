'''
Created on 2020/05/05

@author: ukai
'''
from framework import BuildOrder

class ConcBuildOrder(BuildOrder):
    '''
    classdocs
    '''


    def __init__(self, nIteration, nSeq, nHorizonValueOptimization, nIntervalPolicyOptimization, nBatchPolicyOptimization, nSaveInterval, description, tConstant, nHiddenValueApproximator, sdPolicy, nActionsSampledFromPolicy, amplitudeDv = 0.1):
        '''
        Constructor
        '''
        
        super(ConcBuildOrder, self).__init__(nIteration, nSeq, nHorizonValueOptimization, nIntervalPolicyOptimization, nBatchPolicyOptimization, nSaveInterval, description)
        
        self.tConstant = tConstant
        self.nHiddenValueApproximator = nHiddenValueApproximator
        self.sdPolicy = sdPolicy
        self.nActionsSampledFromPolicy = nActionsSampledFromPolicy
        self.amplitudeDv = amplitudeDv
                
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
            sdPolicy = self.sdPolicy,
            nActionsSampledFromPolicy = self.nActionsSampledFromPolicy,
            amplitudeDv = self.amplitudeDv,
            )