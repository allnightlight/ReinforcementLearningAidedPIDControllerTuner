'''
Created on 2020/05/03

@author: ukai
'''
import unittest

from ConcAction import ConcAction
from ConcAgent import ConcAgent
from ConcObservation import ConcObservation
from ConcRewardGiver import ConcRewardGiver
from ConcValueFunctionApproximator import ConcValueFunctionApproximator
from ConcValueFunctionOptimizer import ConcValueFunctionOptimizer
from MyArray import MyArray
from framework import ObservationSequence
import numpy as np
import tensorflow as tf
from ConcEnvironment import ConcEnvironment


class Test(unittest.TestCase):


    def test001(self):
        
        nHiddenValueApproximator = 2**3
        nHorizonValueOptimization = 3
        
        valueFunctionApproximator = ConcValueFunctionApproximator(nHiddenValueApproximator)
        agent = ConcAgent(ConcEnvironment.nMv)
        
        valueFunctionOptimizer = ConcValueFunctionOptimizer(valueFunctionApproximator, agent, nHorizonValueOptimization)
        
        assert isinstance(valueFunctionOptimizer, ConcValueFunctionOptimizer)
        
        observationSequences = MyArray()
        actions = MyArray()
        rewards = MyArray()
        
        nStep= 10
        nBatch = 2**5
        
        observationSequence = ObservationSequence()
        for _ in range(nStep + 1):
            y = np.random.randn(nBatch, ConcEnvironment.nPv).astype(np.float32) # (*, nPv)
            observationSequence.add(ConcObservation(y))
            observationSequences.add(observationSequence)
            
        for _ in range(nStep):
            action = ConcAction(tf.random.normal(shape = (nBatch, ConcEnvironment.nMv)))
            actions.add(action)
        
        for observationSequence, action in zip(observationSequences, actions):
            reward = ConcRewardGiver().evaluate(observationSequence, action)
            rewards.add(reward)
            
        valueFunctionOptimizer.train(observationSequences, actions, rewards)
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test001']
    unittest.main()