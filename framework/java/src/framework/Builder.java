package framework;

public class Builder {
	
	private Store store;
	private AgentFactory agentFactory;
	private EnvironmentFactory environmentFactory;
	private ValueFunctionApproximatorFactory valueFunctionApproximatorFactory;
	private RewardGiverFactory rewardGiverFactory;	
	private TrainerFactory trainerFactory;
	
	private Agent currentlyTrainedAgent;
	private BuildOrder currentlyTrainedBuildOrder;
	
	private MyLogger myLogger;
		
	public Builder(Store store, AgentFactory agentFactory, EnvironmentFactory environmentFactory, TrainerFactory trainerFactory, ValueFunctionApproximatorFactory valueFunctionApproximatorFactory, RewardGiverFactory rewardGiverFactory, MyLogger myLogger) {
		// TODO Auto-generated constructor stub
		
		this.store                               = store ;
		this.agentFactory                        = agentFactory;
		this.environmentFactory                  = environmentFactory  ;
		this.trainerFactory                      = trainerFactory  ;
		this.valueFunctionApproximatorFactory    = valueFunctionApproximatorFactory ;
		this.rewardGiverFactory                  = rewardGiverFactory ;
		this.myLogger 							 = myLogger;
		
		currentlyTrainedAgent = null;
		currentlyTrainedBuildOrder = null;		
	}
		
	public void build(MyArray<BuildOrder> buildOrders) {

		for (BuildOrder buildOrder : buildOrders) {
			this.buildOneAgent(buildOrder);
		}
		
	}
	
	private void buildOneAgent(BuildOrder buildOrder) {
		this.currentlyTrainedBuildOrder = buildOrder;	
		this.currentlyTrainedAgent = this.agentFactory.create(buildOrder);
		Environment environment = this.environmentFactory.create(buildOrder);
		
		ValueFunctionApproximator valueFunctionApproximator = this.valueFunctionApproximatorFactory.create(buildOrder);
		RewardGiver rewardGiver = this.rewardGiverFactory.create(buildOrder);
		
		Trainer trainer = this.trainerFactory.create(this.currentlyTrainedAgent, 
				environment, 
				valueFunctionApproximator, 
				rewardGiver, 
				buildOrder);
		trainer.requestTrain(this);
		
		this.currentlyTrainedBuildOrder = null;
		this.currentlyTrainedAgent = null;		
	}
	
	public void saveAgent(Trainer trainer) {
		TrainId trainId = TrainId.generateTrainId();
		AgentMemento agentMemento = this.currentlyTrainedAgent.createMemento();
		StoreField storeField = new StoreField(trainer.getTimeSimulation(), agentMemento, this.currentlyTrainedBuildOrder, Utils.generateCurrentDatetimeAsString());
				
		this.store.save(trainId, storeField);
		this.myLogger.info(trainId, storeField);
	}

}
