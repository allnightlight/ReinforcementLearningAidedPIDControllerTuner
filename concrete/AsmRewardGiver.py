'''
Created on 2020/05/26

@author: ukai
'''
import numpy as np
from framework import RewardGiver
from ConcReward import ConcReward
from AsmAction import AsmAction

class AsmRewardGiver(RewardGiver):
    '''
    classdocs
    '''

    def __init__(self, weight = 0.5, SvNh4 = 3.0, penaltyType = 1):
        '''
        Constructor
        '''
        
        self.weight = weight
        self.SvNh4 = SvNh4
        self.penaltyType = penaltyType
        
    def evaluate(self, observationSequence, action):
        assert isinstance(action, AsmAction)
        
        observation = observationSequence[-1]
        S_NH4 = observation.getValue() # (*, nPv)
        
        u = action.getValue() # (*, nMv)
        Do = action.getActionOnEnvironment()[:,0] # (*,)

        if self.penaltyType == 0:        
            # e =
            #     S_NH4 - Sv (S_NH4 > Sv),
            #     0          otherwise.
            e = -1. * np.max(np.concatenate((S_NH4 - self.SvNh4, np.zeros(S_NH4.shape)), axis=-1), axis=-1) # (*,)
            # to minimize the penalty against the excess of NH4 beyond the SV = 3.
        
            e += -1. * Do # (*,) to minimize the cost
            reg = -1. * np.sum(np.abs(u), axis = -1) # (*,) to stabilize the training
            
            r = self.weight * e + (1.0 - self.weight) * reg

        if self.penaltyType == 1:        
            # e =
            #     S_NH4 - Sv (S_NH4 > Sv),
            #     0          otherwise.
            
            e = -1. * np.max(np.abs(S_NH4 - self.SvNh4), axis=-1) # (*,)
            # to make NH4 approach to the SV
        
            reg = -1. * np.sum(np.abs(u), axis = -1) # (*,) to stabilize the training
            
            r = self.weight * e + (1.0 - self.weight) * reg
        
        return ConcReward(r.astype(np.float32))