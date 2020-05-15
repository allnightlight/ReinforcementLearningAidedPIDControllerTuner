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
import tensorflow as tf
from ConcRewardGiverFactory import ConcRewardGiverFactory
from ConcBuildOrder import ConcBuildOrder


class Test(unittest.TestCase):


    def test001(self):
        
        nBatch = 2**5
        r = np.random.randn(nBatch).astype(np.float32)
        reward = ConcReward(r)
        assert np.all(reward.getValue() == r)

    def test002(self):
        
        rewardGiver = ConcRewardGiver()
        assert isinstance(rewardGiver, ConcRewardGiver)

        nLevers = 10        
        action = ConcAction(tf.random.uniform(shape = (1, nLevers,)))
        observationSequence = ObservationSequence()
        
        y = np.array(1.0, np.float32).reshape(1,1)
        observation = ConcObservation(y)
        observationSequence.add(observation)
        
        reward = rewardGiver.evaluate(observationSequence, action)
        
        assert isinstance(reward, ConcReward)
        
        # in this case, reward equals with y.
        assert reward.getValue() == y

    def test003(self):
        
        rewardGiverFactory = ConcRewardGiverFactory()
        assert isinstance(rewardGiverFactory, ConcRewardGiverFactory)
        
        buildOrder = ConcBuildOrder(100, 1, 2, 10, 32, 128, "test", 3)
        
        rewardGiver = rewardGiverFactory.create(buildOrder)
        assert isinstance(rewardGiver, ConcRewardGiver)
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test001']
    unittest.main()