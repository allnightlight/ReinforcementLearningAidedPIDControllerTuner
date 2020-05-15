'''
Created on 2020/05/03

@author: ukai
'''
from framework import PolicyOptimizer, ObservationSequence
import tensorflow as tf


class ConcPolicyOptimizer(PolicyOptimizer):
    '''
    classdocs
    '''


    def __init__(self, agent, valueFunctionApproximator, nIntervalPolicyOptimization, nBatchPolicyOptimization):
        '''
        Constructor
        '''
        super(ConcPolicyOptimizer, self).__init__(agent, valueFunctionApproximator, nIntervalPolicyOptimization, nBatchPolicyOptimization)

        self.optimizer = tf.keras.optimizers.Adam()
        self.countUpdate = 0

            
    def train(self, observationSequences):
        self.countUpdate += 1
        
        assert isinstance(observationSequences, list)
        for observationSequence in observationSequences:
            assert isinstance(observationSequence, ObservationSequence)

        with tf.GradientTape() as gtape:
        
            values = []
            for observationSequence in observationSequences:
                qValue = self.valueFunctionApproximator(observationSequence)
                action = self.agent(observationSequence)
                
                _Q = qValue.getValue() # (*, nLevers)
                _P = action.getValue() # (*, nLevers)
                
                values.append(tf.reduce_sum(_Q * _P, axis=-1))
                
            _ValueAvg = tf.reduce_mean(values) # (,)
            _Loss = - _ValueAvg # to minimize Loss in another words, maximize ValueAvg
        _Grads = gtape.gradient(_Loss, self.agent.trainable_variables)        
        self.optimizer.apply_gradients(zip(_Grads, self.agent.trainable_variables))