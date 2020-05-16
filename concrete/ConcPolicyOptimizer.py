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


    def __init__(self, agent, valueFunctionApproximator, nIntervalPolicyOptimization, nBatchPolicyOptimization, nActionsSampledFromPolicy):
        '''
        Constructor
        '''
        super(ConcPolicyOptimizer, self).__init__(agent, valueFunctionApproximator, nIntervalPolicyOptimization, nBatchPolicyOptimization)

        self.optimizer = tf.keras.optimizers.Adam()
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
                LLsampled = []
                for _ in range(self.nActionsSampledFromPolicy):
                    action = self.agent(observationSequence)
                    qValue = self.valueFunctionApproximator(observationSequence, action)
                    _q = qValue.getValue() # (*, 1)
                    Qsampled.append(_q.numpy())
                    _ll = self.agent.loglikelihood(observationSequence, action) # (*, 1)
                    LLsampled.append(_ll)
                Qsampled = np.stack(Qsampled, axis=0) # (nActionsSampledFromPolicy, *, 1)
                _LLsampled = tf.stack(LLsampled, axis=0) # (nActionsSampledFromPolicy, *, 1)
                V = np.mean(Qsampled, axis=0, keepdims=True) # (*, 1), V(s) = EXP(Q(s,a), over a ~ pi(.|s), say, the policy of the given agent)
                
                values.append(tf.reduce_mean(_LLsampled * (Qsampled - V))) # (,)
                
            _ValueAvg = tf.reduce_mean(values) # (,)
            _Loss = -1.0 *  _ValueAvg # to minimize Loss in another words, maximize ValueAvg
        _Grads = gtape.gradient(_Loss, self.agent.trainable_variables)        
        self.optimizer.apply_gradients(zip(_Grads, self.agent.trainable_variables))