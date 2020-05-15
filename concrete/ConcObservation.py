'''
Created on 2020/05/03

@author: ukai
'''
import numpy as np
from framework import Observation

class ConcObservation(Observation):
    '''
    classdocs
    '''


    def __init__(self, y):
        '''
        Constructor
        '''
        assert isinstance(y, np.ndarray)
        assert len(y.shape) == 2
        assert y.dtype is np.dtype(np.float32)
        self.y = y # (*, Ny = 1)
        
    def getValue(self):
        return self.y # (*, Ny=1)
        