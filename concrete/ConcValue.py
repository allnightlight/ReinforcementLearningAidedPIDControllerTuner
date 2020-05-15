'''
Created on 2020/05/03

@author: ukai
'''
from framework import Value

class ConcValue(Value):
    '''
    classdocs
    '''


    def __init__(self, _qValue):
        '''
        Constructor
        '''
        self._qValue = _qValue # (*, nLevers)
        
    def getValue(self):
        return self._qValue
        