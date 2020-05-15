'''
Created on 2020/05/03

@author: ukai
'''
import tensorflow as tf
from framework import ValueFunctionApproximator
from ConcValue import ConcValue

class ConcValueFunctionApproximator(ValueFunctionApproximator, tf.keras.Model):
    '''
    classdocs
    '''

    def __init__(self, nLevers):
        '''
        Constructor
        '''
        super(ConcValueFunctionApproximator, self).__init__()
        self.dense = tf.keras.layers.Dense(nLevers) # (*, Ny) -> (*, nLevers)

    def call(self, observationSequence):
        observation = observationSequence[-1] # as ConcObservation
        y = observation.getValue() # (*, Ny)
        
        _qValue = self.dense(y) # (*, nLevers)
        
        return ConcValue(_qValue)
        