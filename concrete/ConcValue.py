'''
Created on 2020/05/03

@author: ukai
'''
from framework import Value

class ConcValue(Value):
    '''
    classdocs
    '''


    def __init__(self, _aValue, _sValue):
        '''
        Constructor
        '''
        self._aValue = _aValue # (*, 1), = q(state, action) action-value function
        self._sValue = _sValue # (*, 1), = v(state), state-value function
        
    def getValue(self):
        return (self._aValue, self._sValue)
        