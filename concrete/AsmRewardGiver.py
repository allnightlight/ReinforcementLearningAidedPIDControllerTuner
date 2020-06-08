'''
Created on 2020/05/26

@author: ukai
'''
import numpy as np
from framework import RewardGiver
from ConcReward import ConcReward
from AsmAction import AsmAction
from AsmObservation import AsmObservation

class AsmRewardGiver(RewardGiver):
    '''
    classdocs
    '''

    def __init__(self, weight = 0.5, weightOnCost = 0.5, penaltyType = 1):
        '''
        Constructor
        '''
        
        self.weight = weight
        self.penaltyType = penaltyType
        self.weightOnCost = weightOnCost
        
    def evaluate(self, observationSequence, action):
        assert isinstance(action, AsmAction)
        
        observation = observationSequence[-1]
        assert isinstance(observation, AsmObservation)
        e = observation.getValue() # (*, nPv)
        
        u = action.getValue() # (*, nMv)
        Do = action.getActionOnEnvironment()[:,0] # (*,)

        if self.penaltyType == 0:        
            # cost =
            #     (1-weightOnCost) * (S_NH4 - Sv) (S_NH4 > Sv),
            #         weightOnCost * DO          otherwise.
            cost = -1. * (1. - self.weightOnCost) * np.max(np.concatenate((e, np.zeros(e.shape)), axis=-1), axis=-1) # (*,)
            # to minimize the penalty against the excess of NH4 beyond the SV = 3.
        
            cost[e[:,0] < 0] += -1. * self.weightOnCost * Do[e[:,0] < 0] # (*,) to minimize the cost when NH4 does not excess the SV.
            reg = -1. * np.sum(np.abs(u), axis = -1) # (*,) to stabilize the training
            
            r = self.weight * cost + (1.0 - self.weight) * reg

        if self.penaltyType == 1:        
            # e =
            #     S_NH4 - Sv (S_NH4 > Sv),
            #     0          otherwise.
            
            cost = -1. * np.max(np.abs(e), axis=-1) # (*,)
            # to make NH4 approach to the SV
        
            reg = -1. * np.sum(np.abs(u), axis = -1) # (*,) to stabilize the training
            
            r = self.weight * cost + (1.0 - self.weight) * reg
        
        return ConcReward(r.astype(np.float32))