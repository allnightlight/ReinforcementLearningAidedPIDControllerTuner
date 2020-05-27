'''
Created on 2020/05/05

@author: ukai
'''
from ConcBuildOrder import ConcBuildOrder
from ConcRewardGiver import ConcRewardGiver
from framework import RewardGiverFactory
from AsmRewardGiver import AsmRewardGiver


class ConcRewardGiverFactory(RewardGiverFactory):
    '''
    classdocs
    '''


    def __init__(self):
        super(ConcRewardGiverFactory, self).__init__()
        
    def create(self, buildOrder):
        assert isinstance(buildOrder, ConcBuildOrder)
        
        if buildOrder.environmentName == "ConcEnvironment":
            return ConcRewardGiver(weight=buildOrder.weightOnError)

        if buildOrder.environmentName == "AsmSimulator":        
            return AsmRewardGiver(weight=buildOrder.weightOnError, penaltyType = buildOrder.asmPenaltyType)