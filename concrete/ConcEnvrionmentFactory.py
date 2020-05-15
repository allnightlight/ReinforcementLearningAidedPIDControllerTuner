'''
Created on 2020/05/05

@author: ukai
'''
from ConcBuildOrder import ConcBuildOrder
from ConcEnvironment import ConcEnvironment
from framework import EnvironmentFactory


class ConcEnvironmentFactory(EnvironmentFactory):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        super(ConcEnvironmentFactory, self).__init__()
        
    def create(self, buildOrder):
        assert isinstance(buildOrder, ConcBuildOrder)
        
        return ConcEnvironment(buildOrder.getnLevers())