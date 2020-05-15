package framework;

public class UseCases {
	
	public void case001() {
		Store store = new Store();
		AgentFactory agentFactory = new AgentFactory();
		EnvironmentFactory environmentFactory = new EnvironmentFactory();
		TrainerFactory trainerFactory = new TrainerFactory();
		ValueFunctionApproximatorFactory valueFunctionApproximatorFactory = new ValueFunctionApproximatorFactory();
		RewardGiverFactory rewardGiverFactory = new RewardGiverFactory();
		MyLogger myLogger = new MyLogger();
		
		MyArray<BuildOrder> buildOrders = new MyArray<BuildOrder>();
		for(int i=0;i<10;i++) {
			buildOrders.add(new BuildOrder(100,3,2,10,16,3, ""));
		}
		Builder builder = new Builder(store, agentFactory, environmentFactory, trainerFactory, valueFunctionApproximatorFactory, rewardGiverFactory, myLogger);
		builder.build(buildOrders);
	}
	
	public void case002() {
		
		Store store = new Store();	
		AgentFactory agentFactory = new AgentFactory();
		
		//
		TrainId trainId = new TrainId("test");
		
		StoreField storeField = store.load(trainId);
		
		int timeSimulation = storeField.getTimeSimulation();
		BuildOrder buildOrder = storeField.getBuildOrder();
		AgentMemento agentMemento = storeField.getAgentMemento();
		
		Agent agent = agentFactory.create(buildOrder);
		agent.loadFromMemento(agentMemento);
	}

}
