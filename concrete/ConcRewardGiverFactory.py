'''
Created on 2020/05/05

@author: ukai
'''
from ConcBuildOrder import ConcBuildOrder
from ConcRewardGiver import ConcRewardGiver
from framework import RewardGiverFactory


class ConcRewardGiverFactory(RewardGiverFactory):
    '''
    classdocs
    '''


    def __init__(self):
        super(ConcRewardGiverFactory, self).__init__()
        
    def create(self, buildOrder):
        assert isinstance(buildOrder, ConcBuildOrder)
        
        return ConcRewardGiver()
        