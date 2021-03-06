'''
Created on 2020/05/05

@author: ukai
'''
from ConcBuildOrder import ConcBuildOrder
from ConcEnvironment import ConcEnvironment
from framework import EnvironmentFactory
from AsmSimulator import AsmSimulator


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
        
        if buildOrder.environmentName == "ConcEnvironment":
            return ConcEnvironment(buildOrder.tConstant, buildOrder.amplitudeDv, buildOrder.amplitudePeriodicDv, buildOrder.cyclePeriodicDv)
        
        if buildOrder.environmentName == "AsmSimulator":        
            return AsmSimulator(amplitudePeriodicDv = buildOrder.amplitudePeriodicDv)