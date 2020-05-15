package framework;

public class TrainId {
	
	private String idStr;
	
	public TrainId(String idStr) {
		// TODO Auto-generated constructor stub
		this.idStr = idStr;
	}
	
	static TrainId generateTrainId() {
		String key = Utils.generateRandomString(16);
		TrainId trainId = new TrainId(key);
		return trainId;
	}
	
	@Override
	public String toString() {
		// TODO Auto-generated method stub
		return this.idStr;
	}

}
