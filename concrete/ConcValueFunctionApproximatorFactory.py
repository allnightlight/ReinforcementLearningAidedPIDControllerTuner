'''
Created on 2020/05/05

@author: ukai
'''
from ConcBuildOrder import ConcBuildOrder
from ConcValueFunctionApproximator import ConcValueFunctionApproximator
from framework import ValueFunctionApproximatorFactory


class ConcValueFunctionApproximatorFactory(ValueFunctionApproximatorFactory):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
        super(ConcValueFunctionApproximatorFactory, self).__init__()
        
    def create(self, buildOrder):
        assert isinstance(buildOrder, ConcBuildOrder)
        
        return ConcValueFunctionApproximator(buildOrder.getnLevers())
        