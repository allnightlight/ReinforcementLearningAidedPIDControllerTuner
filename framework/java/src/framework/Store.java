package framework;

public class Store {
		
	public Store() {
		// TODO Auto-generated constructor stub
	}
		
	public void save(TrainId trainId, StoreField storeField) {
	}
	
	public StoreField load(TrainId trainId) {
		return new StoreField(0, new AgentMemento(), new BuildOrder(1, 2, 3, 4, 5, 6, "stub"), "2020-05-05 14:45:59");
	}
	
}
