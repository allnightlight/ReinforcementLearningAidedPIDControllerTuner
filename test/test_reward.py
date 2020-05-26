'''
Created on 2020/05/03

@author: ukai
'''
import unittest

from ConcAction import ConcAction
from ConcObservation import ConcObservation
from ConcReward import ConcReward
from ConcRewardGiver import ConcRewardGiver
from framework import ObservationSequence
import numpy as np
from ConcRewardGiverFactory import ConcRewardGiverFactory
from ConcBuildOrder import ConcBuildOrder
from AsmRewardGiver import AsmRewardGiver
from AsmAction import AsmAction


class Test(unittest.TestCase):


    def test001(self):
        
        nBatch = 2**5
        r = np.random.randn(nBatch).astype(np.float32)
        reward = ConcReward(r)
        assert np.all(reward.getValue() == r)

    def test002(self):
        
        rewardGiver = ConcRewardGiver()
        assert isinstance(rewardGiver, ConcRewardGiver)

        nMv = 10
        nPv = 1        
        action = ConcAction(np.random.randn(1, nMv))
        observationSequence = ObservationSequence()
        
        y = np.random.randn(1, nPv).astype(np.float32)
        observation = ConcObservation(y)
        observationSequence.add(observation)
        
        reward = rewardGiver.evaluate(observationSequence, action)
        
        assert isinstance(reward, ConcReward)
        
        assert np.all(reward.getValue() <= 0.0) # (*,)

    def test003(self):
        
        rewardGiverFactory = ConcRewardGiverFactory()
        assert isinstance(rewardGiverFactory, ConcRewardGiverFactory)
        
        buildOrder = ConcBuildOrder(100, 1, 2, 10, 32, 128, "test", 3, 100, 0.01, 2**3)
        
        rewardGiver = rewardGiverFactory.create(buildOrder)
        assert isinstance(rewardGiver, ConcRewardGiver)
        
    def test004(self):
        # check AsmRewardGiver
        
        SvNh4 = 3
        
        rewardGiver = AsmRewardGiver(SvNh4 = SvNh4)
        assert isinstance(rewardGiver, AsmRewardGiver)

        nMv = 1
        nPv = 1        
        for _ in range(2**7):
            u = np.random.randn(1, nMv).astype(np.float32)
            action = AsmAction(u)
            observationSequence = ObservationSequence()
            
            y = 10 * np.random.rand(1, nPv).astype(np.float32)
            observation = ConcObservation(y)
            observationSequence.add(observation)
            
            rewardGiver.weight = 1.0
            reward = rewardGiver.evaluate(observationSequence, action)
            
            assert isinstance(reward, ConcReward)        
            assert np.all(reward.getValue() <= 0.0) # (*,)        
            assert reward.getValue()[0] == -1. * max(y[0,0] - SvNh4, 0)
            
            rewardGiver.weight = 0.0
            reward = rewardGiver.evaluate(observationSequence, action)
            
            assert isinstance(reward, ConcReward)        
            assert np.all(reward.getValue() <= 0.0) # (*,)        
            assert reward.getValue()[0] == -1. * action.getActionOnEnvironment()[0,0]
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test001']
    unittest.main()