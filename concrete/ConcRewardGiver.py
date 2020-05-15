'''
Created on 2020/05/03

@author: ukai
'''
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
        y = observation.getValue() # in {0, 1} (*, Ny=1)
        r = y[:,0] # (*,)
        return ConcReward(r)