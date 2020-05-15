'''
Created on 2020/05/05

@author: ukai
'''
from framework import MyLogger
from datetime import datetime

class ConcMyLogger(MyLogger):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        super(ConcMyLogger, self).__init__()
        
    def info(self, trainId, storeField):
        msg = "{0}: trainId = {1}, timeSimulation = {2: 5d}, buildOrder.description = {3}".format(
            datetime.strftime(datetime.now(), "%Y/%m/%d %H:%M:%S")
            , trainId.__str__()
            , storeField.getTimeSimulation()
            , storeField.getBuildOrder().getDescription()
            )
        
        print(msg)
    
    
        