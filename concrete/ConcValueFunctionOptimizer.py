'''
Created on 2020/05/03

@author: ukai
'''

import numpy as np
import tensorflow as tf
from framework import ValueFunctionOptimizer
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
        
        A0 = action0.getSelectedAction() # (*, nLevers)
        
        rewardMean = np.mean([reward.getValue() for reward in rewards ], axis=0) # (*,)
            
        with tf.GradientTape() as gtape:            
            qValue0 = self.valueFunctionApproximator(observationSequences[0]) # (*, nLevers)
            
            _Q0 = qValue0.getValue() # (*, nLevers)
        
            _ErrorBellman = tf.reduce_sum(_Q0 * A0, axis=-1) - rewardMean # (*,)
                    
            _Loss = tf.reduce_mean(_ErrorBellman**2) #(,)
        
        _Grad = gtape.gradient(_Loss, self.valueFunctionApproximator.trainable_variables)
        
        self.optimizer.apply_gradients(zip(_Grad, self.valueFunctionApproximator.trainable_variables))