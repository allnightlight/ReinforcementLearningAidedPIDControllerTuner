'''
Created on 2020/05/03

@author: ukai
'''

import numpy as np
import tensorflow as tf
from framework import ValueFunctionApproximator
from ConcValue import ConcValue

class ConcValueFunctionApproximator(ValueFunctionApproximator, tf.keras.Model):
    '''
    classdocs
    '''

    def __init__(self, nHiddenValueApproximator):
        '''
        Constructor
        '''
        super(ConcValueFunctionApproximator, self).__init__()
        
        fnn = tf.keras.Sequential()
        fnn.add(tf.keras.layers.Dense(nHiddenValueApproximator))
        fnn.add(tf.keras.layers.Activation('relu'))        
        fnn.add(tf.keras.layers.Dense(1))
        
        self.fnn = fnn # (*, nPv + nMv) -> (*, 1)

    def call(self, observationSequence, action):
        observation = observationSequence[-1] # as ConcObservation
        
        y = observation.getValue() # (*, nPv)
        u = action.getValue() # (*, nMv)
        uNull = tf.zeros(shape=u.shape) # (*, nMv)
        
        yu = np.concatenate((y,u), axis=-1) # (*, nPv + nMv)
        yuNull = np.concatenate((y,uNull), axis=-1) # (*, nPv + nMv)
        
        _aValue = self.fnn(yu) # (*, 1)
        _sValue = self.fnn(yuNull) # (*, 1)
        
        return ConcValue(_aValue, _sValue)
        