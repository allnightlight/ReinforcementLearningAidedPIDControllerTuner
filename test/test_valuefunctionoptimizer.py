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


class Test(unittest.TestCase):


    def test001(self):
        
        nLevers = 10
        nHorizonValueOptimization = 3
        
        valueFunctionApproximator = ConcValueFunctionApproximator(nLevers)
        agent = ConcAgent(nLevers)
        
        valueFunctionOptimizer = ConcValueFunctionOptimizer(valueFunctionApproximator, agent, nHorizonValueOptimization)
        
        assert isinstance(valueFunctionOptimizer, ConcValueFunctionOptimizer)
        
        observationSequences = MyArray()
        actions = MyArray()
        rewards = MyArray()
        
        Nstep = 10
        Ny = 1
        observationSequence = ObservationSequence()
        for _ in range(Nstep + 1):
            y = np.random.randn(1, Ny).astype(np.float32)
            observationSequence.add(ConcObservation(y))
            observationSequences.add(observationSequence)
            
        for _ in range(Nstep):
            action = ConcAction(tf.random.uniform(shape = (1, nLevers)))
            actions.add(action)
        
        for observationSequence, action in zip(observationSequences, actions):
            reward = ConcRewardGiver().evaluate(observationSequence, action)
            rewards.add(reward)
            
        valueFunctionOptimizer.train(observationSequences, actions, rewards)
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test001']
    unittest.main()