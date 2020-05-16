'''
Created on 2020/05/03

@author: ukai
'''

import numpy as np
import tensorflow as tf
from framework import ValueFunctionOptimizer, ObservationSequence
from ConcAction import ConcAction

class ConcValueFunctionOptimizer(ValueFunctionOptimizer):
    '''
    classdocs
    '''


    def __init__(self, valueFunctionApproximator, agent, nHorizonValueOptimization):
        '''
        Constructor
        '''
        super(ConcValueFunctionOptimizer, self).__init__(valueFunctionApproximator, agent, nHorizonValueOptimization)
        self.optimizer = tf.keras.optimizers.Adam()
        self.countUpdate = 0
        
        
        
    def train(self, observationSequences, actions, rewards):
        self.countUpdate += 1
        
        Nstep = len(actions)
        assert len(observationSequences) == Nstep + 1
        assert len(rewards) == Nstep
        
        action0 = actions[0]
        assert isinstance(action0, ConcAction)
        
        observationSequence0 = observationSequences[0]
        assert isinstance(observationSequence0, ObservationSequence)
            
        rewardMean = np.mean([reward.getValue() for reward in rewards ], axis=0) # (*,)
            
        with tf.GradientTape() as gtape:            
            qValue0 = self.valueFunctionApproximator(observationSequence0, action0) # (*, 1)
            
            _q0 = qValue0.getValue() # (*, 1)
        
            _ErrorBellman = _q0 - rewardMean # (*,)
                    
            _Loss = tf.reduce_mean(_ErrorBellman**2) #(,)
        
        _Grad = gtape.gradient(_Loss, self.valueFunctionApproximator.trainable_variables)
        
        self.optimizer.apply_gradients(zip(_Grad, self.valueFunctionApproximator.trainable_variables))