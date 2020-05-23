'''
Created on 2020/05/03

@author: ukai
'''
import numpy as np
from framework import PolicyOptimizer, ObservationSequence
import tensorflow as tf


class ConcPolicyOptimizer(PolicyOptimizer):
    '''
    classdocs
    '''


    def __init__(self, agent, valueFunctionApproximator, nIntervalPolicyOptimization, nBatchPolicyOptimization, nActionsSampledFromPolicy, optimizer = "Adam", learningRate = 1e-3):
        '''
        Constructor
        '''
        super(ConcPolicyOptimizer, self).__init__(agent, valueFunctionApproximator, nIntervalPolicyOptimization, nBatchPolicyOptimization)

        self.optimizer = None
        if optimizer == "Adam":
            self.optimizer = tf.keras.optimizers.Adam(learning_rate = learningRate)
        if optimizer == "RMSprop":
            self.optimizer = tf.keras.optimizers.RMSprop(learning_rate = learningRate)            
        self.countUpdate = 0
        self.nActionsSampledFromPolicy = nActionsSampledFromPolicy

            
    def train(self, observationSequences):
        self.countUpdate += 1
        
        assert isinstance(observationSequences, list)
        for observationSequence in observationSequences:
            assert isinstance(observationSequence, ObservationSequence)

        with tf.GradientTape() as gtape:
            
            values = []            
            for observationSequence in observationSequences:
                Qsampled = []
                V = None
                LLsampled = []
                for k1 in range(self.nActionsSampledFromPolicy):
                    action = self.agent(observationSequence)
                    qValue = self.valueFunctionApproximator(observationSequence, action)
                    _q, _sValue = qValue.getValue() # _q = (*, 1), _sValue = (*,1)
                    Qsampled.append(_q.numpy())
                    if k1 == 0:
                        V = _sValue.numpy() # (*,1)
                    _ll = self.agent.loglikelihood(observationSequence, action) # (*, 1)
                    LLsampled.append(_ll)
                Qsampled = np.stack(Qsampled, axis=0) # (nActionsSampledFromPolicy, *, 1)
                _LLsampled = tf.stack(LLsampled, axis=0) # (nActionsSampledFromPolicy, *, 1)
                
                values.append(tf.reduce_mean(_LLsampled * (Qsampled - V))) # (,)
                
            _ValueAvg = tf.reduce_mean(values) # (,)
            _Loss = -1.0 *  _ValueAvg # to minimize Loss in another words, maximize ValueAvg
        _Grads = gtape.gradient(_Loss, self.agent.trainable_variables)        
        self.optimizer.apply_gradients(zip(_Grads, self.agent.trainable_variables))