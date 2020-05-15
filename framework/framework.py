from MyArray import MyArray
from Utils import Utils


""" generated source for module Action """
# package: framework
class Action(object):

    def __init__(self):
        """ generated source for method __init__ """
        #  TODO Auto-generated constructor stub

    def getValue(self):
        """ generated source for method getValue """
        return self.value



""" generated source for module Agent """
# package: framework
class Agent(object):
    def createMemento(self):
        """ generated source for method createMemento """
        return AgentMemento()

    def loadFromMemento(self, agentMemento):
        """ generated source for method loadFromMemento """
        return

    def call(self, observationSequence):
        """ generated source for method call """
        return Action()



""" generated source for module AgentFactory """
# package: framework
class AgentFactory(object):
    def __init__(self):
        """ generated source for method __init__ """
        #  TODO Auto-generated constructor stub

    def create(self, buildOrder):
        """ generated source for method create """
        return Agent()



""" generated source for module AgentMemento """
# package: framework
class AgentMemento(object):
    """ generated source for class AgentMemento """



""" generated source for module Builder """
# package: framework
class Builder(object):

    def __init__(self, store, agentFactory, environmentFactory, trainerFactory, valueFunctionApproximatorFactory, rewardGiverFactory, myLogger):
        """ generated source for method __init__ """
        #  TODO Auto-generated constructor stub
        self.store = store
        self.agentFactory = agentFactory
        self.environmentFactory = environmentFactory
        self.trainerFactory = trainerFactory
        self.valueFunctionApproximatorFactory = valueFunctionApproximatorFactory
        self.rewardGiverFactory = rewardGiverFactory
        self.myLogger = myLogger
        self.currentlyTrainedAgent = None
        self.currentlyTrainedBuildOrder = None

    def build(self, buildOrders):
        """ generated source for method build """
        for buildOrder in buildOrders:
            self.buildOneAgent(buildOrder)

    def buildOneAgent(self, buildOrder):
        """ generated source for method buildOneAgent """
        self.currentlyTrainedBuildOrder = buildOrder
        self.currentlyTrainedAgent = self.agentFactory.create(buildOrder)
        environment = self.environmentFactory.create(buildOrder)
        valueFunctionApproximator = self.valueFunctionApproximatorFactory.create(buildOrder)
        rewardGiver = self.rewardGiverFactory.create(buildOrder)
        trainer = self.trainerFactory.create(self.currentlyTrainedAgent, environment, valueFunctionApproximator, rewardGiver, buildOrder)
        trainer.requestTrain(self)
        self.currentlyTrainedBuildOrder = None
        self.currentlyTrainedAgent = None

    def saveAgent(self, trainer):
        """ generated source for method saveAgent """
        trainId = TrainId.generateTrainId()
        agentMemento = self.currentlyTrainedAgent.createMemento()
        storeField = StoreField(trainer.getTimeSimulation(), agentMemento, self.currentlyTrainedBuildOrder, Utils.generateCurrentDatetimeAsString())
        self.store.save(trainId, storeField)
        self.myLogger.info(trainId, storeField)



""" generated source for module BuildOrder """
# package: framework
class BuildOrder(object):

    def __init__(self, nIteration, nSeq, nHorizonValueOptimization, nIntervalPolicyOptimization, nBatchPolicyOptimization, nSaveInterval, description):
        """ generated source for method __init__ """
        #  TODO Auto-generated constructor stub
        self.nIteration = nIteration
        self.nSeq = nSeq
        self.nHorizonValueOptimization = nHorizonValueOptimization
        self.nIntervalPolicyOptimization = nIntervalPolicyOptimization
        self.nBatchPolicyOptimization = nBatchPolicyOptimization
        self.nSaveInterval = nSaveInterval
        self.description = description

    def getnIteration(self):
        """ generated source for method getnIteration """
        return self.nIteration

    def getnSeq(self):
        """ generated source for method getnSeq """
        return self.nSeq

    def getnHorizonValueOptimization(self):
        """ generated source for method getnHorizonValueOptimization """
        return self.nHorizonValueOptimization

    def getnIntervalPolicyOptimization(self):
        """ generated source for method getnIntervalPolicyOptimization """
        return self.nIntervalPolicyOptimization

    def getnBatchPolicyOptimization(self):
        """ generated source for method getnBatchPolicyOptimization """
        return self.nBatchPolicyOptimization

    def getnSaveInterval(self):
        """ generated source for method getnSaveInterval """
        return self.nSaveInterval

    def getDescription(self):
        """ generated source for method getDescription """
        return self.description



""" generated source for module ClosedLoopSimulator """
# package: framework
class ClosedLoopSimulator(object):

    def __init__(self, environment, agent, nSeq):
        """ generated source for method __init__ """
        #  TODO Auto-generated constructor stub
        self.agent = agent
        self.environment = environment
        self.observationSequenceLast = ObservationSequence()
        self.nSeq = nSeq
        self.actionLast = None
        self.observationSequencePrev = None

    def init(self):
        """ generated source for method init """
        self.environment.init()
        self.observationSequenceLast.clear()
        self.observationSequencePrev = self.observationSequenceLast.copy()
        observation = self.environment.observe()
        self.observationSequenceLast.add(observation)

    def update(self):
        """ generated source for method update """
        self.observationSequencePrev = self.observationSequenceLast.copy()
        self.actionLast = self.agent.call(self.observationSequenceLast)
        self.environment.update(self.actionLast)
        observation = self.environment.observe()
        if len(self.observationSequenceLast) >= self.nSeq:
            self.observationSequenceLast.remove(0)
        self.observationSequenceLast.add(observation)

    def requestInit(self, trainer):
        """ generated source for method requestInit """
        self.init()
        trainer.addObservationSequence(self.observationSequenceLast.copy())
        trainer.setTimeLastUpdate(-1)
        trainer.setTimeSimulation(-1)

    def requestUpdate(self, trainer):
        """ generated source for method requestUpdate """
        self.update()
        rewardLast = trainer.reward(self.observationSequencePrev, self.actionLast)
        trainer.addObservationSequence(self.observationSequenceLast.copy())
        trainer.addAction(self.actionLast)
        trainer.addReward(rewardLast)
        trainer.addTimeSimulation()



""" generated source for module Environment """
# package: framework
class Environment(object):
    def init(self):
        """ generated source for method init """

    def update(self, action):
        """ generated source for method update """

    def observe(self):
        """ generated source for method observe """
        return Observation()



""" generated source for module EnvironmentFactory """
# package: framework
class EnvironmentFactory(object):
    def __init__(self):
        """ generated source for method __init__ """
        #  TODO Auto-generated constructor stub

    def create(self, buildOrder):
        """ generated source for method create """
        return Environment()



""" generated source for module MyLogger """
# package: framework
class MyLogger(object):
    def info(self, trainId, storeField):
        """ generated source for method info """



""" generated source for module Observation """
# package: framework
class Observation(object):

    def __init__(self):
        """ generated source for method __init__ """
        #  TODO Auto-generated constructor stub

    def getValue(self):
        """ generated source for method getValue """
        return self.value



""" generated source for module ObservationSequence """
# package: framework
class ObservationSequence(MyArray, Observation):
    def copy(self):
        """ generated source for method copy """
        return ObservationSequence(self.clone())



""" generated source for module PolicyOptimizer """
# package: framework
class PolicyOptimizer(object):

    def __init__(self, agent, valueFunctionApproximator, nIntervalPolicyOptimization, nBatchPolicyOptimization):
        """ generated source for method __init__ """
        #  TODO Auto-generated constructor stub
        self.agent = agent
        self.valueFunctionApproximator = valueFunctionApproximator
        self.nBatchPolicyOptimization = nBatchPolicyOptimization
        self.nIntervalPolicyOptimization = nIntervalPolicyOptimization

    def train(self, observationSequences):
        """ generated source for method train """
        #  NOT IMPLEMENTED YET

    def requestUpdate(self, trainer):
        """ generated source for method requestUpdate """
        nSample = 0
        observationSequences = None
        if (trainer.getTimeSimulation() + 1) % self.nIntervalPolicyOptimization == 0:
            observationSequences = MyArray()
            nSample = trainer.getTimeSimulation() + 2
            for i in Utils.myRandomRrandint(0, nSample, self.nBatchPolicyOptimization):
                observationSequences.add(trainer.getObservationSequence(i))
            self.train(observationSequences)
            trainer.markPolicyUpdate()



""" generated source for module Reward """
# package: framework
class Reward(object):

    def __init__(self):
        """ generated source for method __init__ """
        #  TODO Auto-generated constructor stub

    def getValue(self):
        """ generated source for method getValue """
        return self.value



""" generated source for module RewardGiver """
# package: framework
class RewardGiver(object):
    def evaluate(self, observationSequence, action):
        """ generated source for method evaluate """
        return Reward()



""" generated source for module RewardGiverFactory """
# package: framework
class RewardGiverFactory(object):
    def __init__(self):
        """ generated source for method __init__ """
        #  TODO Auto-generated constructor stub

    def create(self, buildOrder):
        """ generated source for method create """
        return RewardGiver()



""" generated source for module Store """
# package: framework
class Store(object):
    def __init__(self):
        """ generated source for method __init__ """
        #  TODO Auto-generated constructor stub

    def save(self, trainId, storeField):
        """ generated source for method save """

    def load(self, trainId):
        """ generated source for method load """
        return StoreField(0, AgentMemento(), BuildOrder(1, 2, 3, 4, 5, 6, "stub"), "2020-05-05 14:45:59")



""" generated source for module StoreField """
# package: framework
class StoreField(object):

    def __init__(self, timeSimulation, agentMemento, buildOrder, timeStamp):
        """ generated source for method __init__ """
        #  TODO Auto-generated constructor stub
        self.timeSimulation = timeSimulation
        self.agentMemento = agentMemento
        self.buildOrder = buildOrder
        self.timeStamp = timeStamp

    def getAgentMemento(self):
        """ generated source for method getAgentMemento """
        return self.agentMemento

    def getTimeSimulation(self):
        """ generated source for method getTimeSimulation """
        return self.timeSimulation

    def getBuildOrder(self):
        """ generated source for method getBuildOrder """
        return self.buildOrder

    def getTimeStamp(self):
        """ generated source for method getTimeStamp """
        return self.timeStamp



""" generated source for module Trainer """
# package: framework
class Trainer(object):

    def __init__(self, closedLoopSimulator, valueFunctionOptimizer, policyOptimizer, rewardGiver, nIteration, nSaveInterval):
        """ generated source for method __init__ """
        #  TODO Auto-generated constructor stub
        self.closedLoopSimulator = closedLoopSimulator
        self.valueFunctionOptimizer = valueFunctionOptimizer
        self.policyOptimizer = policyOptimizer
        self.rewardGiver = rewardGiver
        self.nIteration = nIteration
        self.nSaveInterval = nSaveInterval
        self.historyActions = MyArray()
        self.historyObservationSequences = MyArray()
        self.historyRewards = MyArray()

    def init(self):
        """ generated source for method init """
        self.historyActions.clear()
        self.historyObservationSequences.clear()
        self.historyRewards.clear()
        self.closedLoopSimulator.requestInit(self)

    def train(self, nIterationLocal):
        """ generated source for method train """
        #  TODO Auto-generated constructor stub
        i = 0
        while i < nIterationLocal:
            #  TODO Auto-generated constructor stub
            self.closedLoopSimulator.requestUpdate(self)
            self.valueFunctionOptimizer.requestUpdate(self)
            self.policyOptimizer.requestUpdate(self)
            i += 1

    def requestTrain(self, builder):
        """ generated source for method requestTrain """
        self.init()
        cnt = 0
        while True:
            if cnt < self.nIteration:
                builder.saveAgent(self)
                self.train(self.nSaveInterval)
                cnt += self.nSaveInterval
            else:
                builder.saveAgent(self)
                break

    def addObservationSequence(self, observationSequence):
        """ generated source for method addObservationSequence """
        self.historyObservationSequences.add(observationSequence)

    def addAction(self, action):
        """ generated source for method addAction """
        self.historyActions.add(action)

    def addReward(self, reward):
        """ generated source for method addReward """
        self.historyRewards.add(reward)

    def getObservationSequence(self, idx):
        """ generated source for method getObservationSequence """
        return self.historyObservationSequences.get(idx)

    def getAction(self, idx):
        """ generated source for method getAction """
        return self.historyActions.get(idx)

    def getReward(self, idx):
        """ generated source for method getReward """
        return self.historyRewards.get(idx)

    def reward(self, observationSequence, action):
        """ generated source for method reward """
        return self.rewardGiver.evaluate(observationSequence, action)

    def addTimeSimulation(self):
        """ generated source for method addTimeSimulation """
        self.timeSimulation += 1

    def markPolicyUpdate(self):
        """ generated source for method markPolicyUpdate """
        self.timeLastUpdate = self.timeSimulation

    def getTimeSimulation(self):
        """ generated source for method getTimeSimulation """
        return self.timeSimulation

    def getTimeLastUpdate(self):
        """ generated source for method getTimeLastUpdate """
        return self.timeLastUpdate

    def setTimeSimulation(self, timeSimulation):
        """ generated source for method setTimeSimulation """
        self.timeSimulation = timeSimulation

    def setTimeLastUpdate(self, timeLastUpdate):
        """ generated source for method setTimeLastUpdate """
        self.timeLastUpdate = timeLastUpdate



""" generated source for module TrainerFactory """
# package: framework
class TrainerFactory(object):
    def __init__(self):
        """ generated source for method __init__ """
        #  TODO Auto-generated constructor stub

    def create(self, agent, environment, valueFunctionApproximator, rewardGiver, buildOrder):
        """ generated source for method create """
        closedLoopSimulator = ClosedLoopSimulator(environment, agent, buildOrder.getnSeq())
        valueFunctionOptimizer = ValueFunctionOptimizer(valueFunctionApproximator, agent, buildOrder.getnHorizonValueOptimization())
        policyOptimizer = PolicyOptimizer(agent, valueFunctionApproximator, buildOrder.getnIntervalPolicyOptimization(), buildOrder.getnBatchPolicyOptimization())
        return Trainer(closedLoopSimulator, valueFunctionOptimizer, policyOptimizer, rewardGiver, buildOrder.getnIteration(), buildOrder.getnSaveInterval())



""" generated source for module TrainId """
# package: framework
class TrainId(object):

    def __init__(self, idStr):
        """ generated source for method __init__ """
        #  TODO Auto-generated constructor stub
        self.idStr = idStr

    @classmethod
    def generateTrainId(cls):
        """ generated source for method generateTrainId """
        key = Utils.generateRandomString(16)
        trainId = TrainId(key)
        return trainId

    def __str__(self):
        """ generated source for method toString """
        #  TODO Auto-generated method stub
        return self.idStr



""" generated source for module UseCases """
# package: framework
class UseCases(object):
    def case001(self):
        """ generated source for method case001 """
        store = Store()
        agentFactory = AgentFactory()
        environmentFactory = EnvironmentFactory()
        trainerFactory = TrainerFactory()
        valueFunctionApproximatorFactory = ValueFunctionApproximatorFactory()
        rewardGiverFactory = RewardGiverFactory()
        myLogger = MyLogger()
        buildOrders = MyArray()
        i = 0
        while i < 10:
            buildOrders.add(BuildOrder(100, 3, 2, 10, 16, 3, ""))
            i += 1
        builder = Builder(store, agentFactory, environmentFactory, trainerFactory, valueFunctionApproximatorFactory, rewardGiverFactory, myLogger)
        builder.build(buildOrders)

    def case002(self):
        """ generated source for method case002 """
        store = Store()
        agentFactory = AgentFactory()
        # 
        trainId = TrainId("test")
        storeField = store.load(trainId)
        timeSimulation = storeField.getTimeSimulation()
        buildOrder = storeField.getBuildOrder()
        agentMemento = storeField.getAgentMemento()
        agent = agentFactory.create(buildOrder)
        agent.loadFromMemento(agentMemento)



""" generated source for module Value """
# package: framework
class Value(object):

    def __init__(self):
        """ generated source for method __init__ """
        #  TODO Auto-generated constructor stub

    def getValue(self):
        """ generated source for method getValue """
        return self.value



""" generated source for module ValueFunctionApproximator """
# package: framework
class ValueFunctionApproximator(object):
    def call(self, observationSequence):
        """ generated source for method call """
        return Value()



""" generated source for module ValueFunctionApproximatorFactory """
# package: framework
class ValueFunctionApproximatorFactory(object):
    def __init__(self):
        """ generated source for method __init__ """
        #  TODO Auto-generated constructor stub

    def create(self, buildOrder):
        """ generated source for method create """
        return ValueFunctionApproximator()



""" generated source for module ValueFunctionOptimizer """
# package: framework
class ValueFunctionOptimizer(object):

    def __init__(self, valueFunctionApproximator, agent, nHorizonValueOptimization):
        """ generated source for method __init__ """
        #  TODO Auto-generated constructor stub
        self.valueFunctionApproximator = valueFunctionApproximator
        self.agent = agent
        self.nHorizonValueOptimization = nHorizonValueOptimization

    def train(self, observationSequences, actions, rewards):
        """ generated source for method train """
        #  NOT IMPLEMENTED YET

    def requestUpdate(self, trainer):
        """ generated source for method requestUpdate """
        timeLastUpdate = trainer.getTimeLastUpdate()
        timeSimulation = trainer.getTimeSimulation()
        observationSequences = None
        actions = None
        rewards = None
        timeBegin = 0
        j = 0
        if timeLastUpdate + self.nHorizonValueOptimization <= timeSimulation:
            observationSequences = MyArray()
            actions = MyArray()
            rewards = MyArray()
            timeBegin = timeSimulation - self.nHorizonValueOptimization + 1
            #  TODO Auto-generated constructor stub
            #  NOT IMPLEMENTED YET
            while j < self.nHorizonValueOptimization:
                #  TODO Auto-generated constructor stub
                #  NOT IMPLEMENTED YET
                observationSequences.add(trainer.getObservationSequence(timeBegin + j))
                actions.add(trainer.getAction(timeBegin + j))
                rewards.add(trainer.getReward(timeBegin + j))
                j += 1
            observationSequences.add(trainer.getObservationSequence(timeBegin + self.nHorizonValueOptimization))
            self.train(observationSequences, actions, rewards)


