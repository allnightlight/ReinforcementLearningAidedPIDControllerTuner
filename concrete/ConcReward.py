'''
Created on 2020/05/03

@author: ukai
'''
import numpy as np
from framework import Reward

class ConcReward(Reward):
    '''
    classdocs
    '''


    def __init__(self, value):
        '''
        Constructor
        '''
        super(ConcReward, self).__init__()
        assert isinstance(value, np.ndarray)
        assert len(value.shape) == 1
        assert value.dtype is np.dtype(np.float32)
        self.value = value# (*,)
        
    def getValue(self):
        return self.value # (*, 1)
        