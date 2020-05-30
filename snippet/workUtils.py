import os
import sqlite3
from glob import glob
from datetime import datetime 

import sys
sys.path.append(os.path.abspath("../framework"))
sys.path.append(os.path.abspath("../concrete"))

from ConcStore import ConcStore
from framework import TrainId, StoreField


def loadTrainLog(trainLogFolderPath, dbName = "trainLog.sqlite"):

    dbAlreadyExists = os.path.exists(dbName)

    conn = sqlite3.connect(dbName)
    cur = conn.cursor()

    if not dbAlreadyExists:
        cur.executescript("""

Create Table SubTableTrainLog
(
    id Integer Primary Key,
    buildOrderId Integer, /* foregin id to the subtable build order */
    trainId   Text Unique, /* accord to a trained agent along with a simulation time*/
    timeSimulation Integer,
    timestamp timestamp
);

Create Table SubTableBuildOrder
(
    id Integer Primary Key,
    buildOrderId Text Unique
);

Create View TrainLog As
    Select 
        t.trainId
        , b.buildOrderId
        , t.timeSimulation
        , t.timestamp
        from SubTableTrainLog t
            inner join SubTableBuildOrder b
                on b.id == t.buildOrderId;
    """)

    concStore = ConcStore()
    for filePath in glob(os.path.join(trainLogFolderPath, "*")):
        trainIdStr = os.path.basename(filePath)
        
        cur.execute('''
Select Exists (
    Select 1 
        From SubTableTrainLog
        Where trainId = ?
        )''', (
        trainIdStr,))

        if cur.fetchone()[0] == 1: # the given train id has already existed in the DB
            continue
        
        trainId = TrainId(trainIdStr)
        
        assert isinstance(trainId, TrainId)
        storeField = concStore.load(trainId) # storeField contains: agentMement, buildOrder
        assert isinstance(storeField, StoreField)
        
        buildOrderIdStr = storeField.getBuildOrder().description # like "abcdefg"
        
        cur.execute('''
            Insert Or Ignore Into SubTableBuildOrder (
                buildOrderId) values (?)''', (
                buildOrderIdStr,
            ))
        cur.execute('''
            Select id
                From SubTableBuildOrder
                Where buildOrderId = ?''', (
                buildOrderIdStr,
            ))
        buildOrderIdInt = cur.fetchone()[0]
        
        cur.execute('''
            Insert Into SubTableTrainLog (
            buildOrderId
            , trainId
            , timeSimulation
            , timestamp)
            values (?, ?, ?, ?)''', (
            buildOrderIdInt
            , trainIdStr
            , storeField.getTimeSimulation()
            , datetime.strptime(storeField.getTimeStamp(), "%Y-%m-%d %H:%M:%S")
        ))
    conn.commit()

    return cur
