'''
Created on 2020/05/03

@author: ukai
'''

from framework import Action
import numpy as np


class ConcAction(Action):
    '''
    classdocs
    '''

    def __init__(self, _u):
        '''
        Constructor
        '''
        assert len(_u.shape) == 2 
        self._u = _u # (*, nMv,)
        
        # _u is not used as a manipulated value for the environment,
        # instead, what should be used is the value ceiling u   
        # after having converted as numpy.ndarray 
        self.actionOnEnvironment = np.tanh(_u.numpy()).astype(np.float32) # (*, nMv,)
        
    def getValue(self):
        return self._u # (*, nMv,)
    
    def getActionOnEnvironment(self):
        return self.actionOnEnvironment # (*, nMv,)