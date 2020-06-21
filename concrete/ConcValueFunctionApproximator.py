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

    def __init__(self, nHiddenValueApproximator, enable_i_component = False, enable_d_component = False):
        '''
        Constructor
        '''
        super(ConcValueFunctionApproximator, self).__init__()
        
        fnn = tf.keras.Sequential()
        fnn.add(tf.keras.layers.Dense(nHiddenValueApproximator))
        fnn.add(tf.keras.layers.Activation('relu'))        
        fnn.add(tf.keras.layers.Dense(1))
        
        self.fnn = fnn # (*, nPv + nMv) -> (*, 1)
        self.enable_i_component = enable_i_component        
        self.enable_d_component = enable_d_component


    def call(self, observationSequence, action):
        observation = observationSequence[-1] # as ConcObservation
        y = observation.getValue() # (*, nPv)
        
        Y = []
        for obserbation in observationSequence:
            Y.append(obserbation.getValue())
        Ynumpy = np.stack(Y, axis=-1) # (*, nPv, nSeq)
        nSeq = len(Y)
        
        if not self.enable_i_component:
            y_i = np.zeros((y.shape[0], 0)).astype(np.float32) # (*, 0)
        elif nSeq > 1:
            y_i = np.sum(Ynumpy, axis=-1) # (*, nPv)
        else:
            y_i = np.zeros(y.shape).astype(np.float32) # (*, nPv)
            
        if not self.enable_d_component:            
            y_d = np.zeros((y.shape[0], 0)).astype(np.float32) # (*, 0)
        elif nSeq > 1:
            t = np.linspace(-(nSeq-1)/2, (nSeq-1)/2, nSeq).astype(np.float32)
            y_d = np.sum(Ynumpy * t, axis=-1)/np.sum(t*t) # (*, nPv)            
        else:
            y_d = np.zeros(y.shape).astype(np.float32) # (*, nPv)
                    
        
        u = action.getValue() # (*, nMv)
        uNull = tf.zeros(shape=u.shape) # (*, nMv)
        
        yu = np.concatenate((y,y_i,y_d,u), axis=-1) # (*, nPv + nMv)
        yuNull = np.concatenate((y,y_i,y_d,uNull), axis=-1) # (*, nPv + nMv)
        
        _aValue = self.fnn(yu) # (*, 1)
        _sValue = self.fnn(yuNull) # (*, 1)
        
        return ConcValue(_aValue, _sValue)
        