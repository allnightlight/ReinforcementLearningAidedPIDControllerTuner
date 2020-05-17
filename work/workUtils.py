import os
import sqlite3
from glob import glob
from datetime import datetime 

import sys
sys.path.append(os.path.abspath("../framework"))
sys.path.append(os.path.abspath("../concrete"))

from ConcStore import ConcStore
from framework import TrainId, StoreField


def loadTrainLog(trainLogFolderPath):

    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()

    cur.execute("""

    Create Table TrainLog
    (
        buildOrderId Text, /* accord to a build order */
        trainId   Text, /* accord to a trained agent along with a simulation time*/
        timeSimulation Integer,
        timestamp timestamp
    )
    """)

    concStore = ConcStore()
    for filePath in glob(os.path.join(trainLogFolderPath, "*")):
        trainId = TrainId(os.path.basename(filePath))
        assert isinstance(trainId, TrainId)
        storeField = concStore.load(trainId) # storeField contains: agentMement, buildOrder
        assert isinstance(storeField, StoreField)
        
        cur.execute('''
        Insert Into TrainLog (buildOrderId, trainId, timeSimulation, timestamp)
        values (?, ?, ?, ?)
        ''', (
            storeField.getBuildOrder().description
            , str(trainId)
            , storeField.getTimeSimulation()
            , datetime.strptime(storeField.getTimeStamp(), "%Y-%m-%d %H:%M:%S")
        ))    

    return cur


trainLogFolderPath = "./trainLog"
cur = loadTrainLog(trainLogFolderPath)

