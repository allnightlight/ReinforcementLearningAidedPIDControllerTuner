'''
Created on 2020/05/03

@author: ukai
'''
import numpy as np
from framework import RewardGiver
from ConcReward import ConcReward

class ConcRewardGiver(RewardGiver):
    '''
    classdocs
    '''


    def __init__(self, weight = 0.5):
        '''
        Constructor
        '''
        
        self.weight = weight
        
    def evaluate(self, observationSequence, action):
        observation = observationSequence[-1]
        y = observation.getValue() # (*, nPv)
        e = -1. *  np.max(np.abs(y), axis=-1) # (*,)
        
        u = action.getValue() # (*, nMv)
        reg = -1. * np.sum(np.abs(u), axis=-1) # (*,)
        
        r = self.weight * e + (1.0 - self.weight) * reg
        
        return ConcReward(r)