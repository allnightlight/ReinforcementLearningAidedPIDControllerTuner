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


    def __init__(self, valueFunctionApproximator, agent, nHorizonValueOptimization, optimizer = "Adam", learningRate=1e-3, returnType = "SumOfFiniteRewardSeries", gamma = None):
        '''
        Constructor
        '''
        super(ConcValueFunctionOptimizer, self).__init__(valueFunctionApproximator, agent, nHorizonValueOptimization)
        self.optimizer = None
        if optimizer == "Adam":
            self.optimizer = tf.keras.optimizers.Adam(learning_rate = learningRate)
        if optimizer == "RMSprop":
            self.optimizer = tf.keras.optimizers.RMSprop(learning_rate = learningRate)            
        self.countUpdate = 0
        self.returnType = returnType
        if returnType == "SumOfInfiniteRewardSeries":
            assert gamma is not None
        self.gamma = gamma

    def trainWithSumOfFiniteRewardSeries(self, observationSequences, actions, rewards):

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
            
            _q0, _sValue0 = qValue0.getValue() # _q0 = (*, 1), _sValue0 = (*,1)
        
            _ErrorBellman = _q0 - rewardMean # (*,)
            _ErrorBellmanForStateValueFunction = _sValue0 - rewardMean # (*,)
                    
            _Loss = tf.reduce_mean(_ErrorBellman**2) + tf.reduce_mean(_ErrorBellmanForStateValueFunction**2) #(,)
        
        _Grad = gtape.gradient(_Loss, self.valueFunctionApproximator.trainable_variables)
        
        self.optimizer.apply_gradients(zip(_Grad, self.valueFunctionApproximator.trainable_variables))

    def trainWithSumOfInfiniteRewardSeries(self, observationSequences, actions, rewards):
        
        Nstep = len(actions)
        assert len(observationSequences) == Nstep + 1
        assert len(rewards) == Nstep
        
        action0 = actions[0]
        assert isinstance(action0, ConcAction)
        
        observationSequence0 = observationSequences[0]
        observationSequence1 = observationSequences[-1]        
        assert isinstance(observationSequence0, ObservationSequence)
        assert isinstance(observationSequence1, ObservationSequence)
               
        gammaExponents = [ self.gamma**k1 for k1 in range(self.nHorizonValueOptimization+1)] # (nHor+1,)
        # gammaExponents = (1, gamma, gamma^2, ..., gamma^(nHor-1), gamma^nHor), where gamma = 1 - 1/nHor.
        
        rewardMean = (1-self.gamma) * np.sum([reward.getValue() * gammaExponent for reward, gammaExponent in zip(rewards, gammaExponents) ], axis=0) # (*,)
        # rewardMean = (1-gamma) * (reward(0) + gamma * reward(1) + ... + gamma^(nHor-1) * reward(nHor-1))
        
        action1 = self.agent(observationSequence1)
             
        with tf.GradientTape() as gtape:
                        
            qValue0 = self.valueFunctionApproximator(observationSequence0, action0) # (*, 1)
            qValue1 = self.valueFunctionApproximator(observationSequence1, action1) # (*, 1)
            
            _q0, _sValue0 = qValue0.getValue() # _q0 = (*, 1), _sValue0 = (*,1)
            _q1, _sValue1 = qValue1.getValue() # _q1 = (*, 1), _sValue1 = (*,1)
        
            _ErrorBellman = _q0 - (rewardMean + gammaExponents[-1] * _q1)# (*,)
            _ErrorBellmanForStateValueFunction = _sValue0 - (rewardMean + gammaExponents[-1] * _sValue1) # (*,)
                    
            _Loss = tf.reduce_mean(_ErrorBellman**2) + tf.reduce_mean(_ErrorBellmanForStateValueFunction**2) #(,)
        
        _Grad = gtape.gradient(_Loss, self.valueFunctionApproximator.trainable_variables)
        
        self.optimizer.apply_gradients(zip(_Grad, self.valueFunctionApproximator.trainable_variables))
        
    def train(self, observationSequences, actions, rewards):
        
        self.countUpdate += 1
        
        if self.returnType == "SumOfFiniteRewardSeries":
            self.trainWithSumOfFiniteRewardSeries(observationSequences, actions, rewards)
        if self.returnType == "SumOfInfiniteRewardSeries":
            self.trainWithSumOfInfiniteRewardSeries(observationSequences, actions, rewards)