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


    def __init__(self):
        '''
        Constructor
        '''
        
    def evaluate(self, observationSequence, action):
        observation = observationSequence[-1]
        y = observation.getValue() # (*, nPv=1)
        r = -1. *  np.max(np.abs(y), axis=-1) # (*,)
        return ConcReward(r)