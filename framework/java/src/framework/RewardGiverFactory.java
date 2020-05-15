package framework;

public class RewardGiverFactory {
		
	public RewardGiverFactory() {
		// TODO Auto-generated constructor stub
	}
	
	public RewardGiver create(BuildOrder buildOrder) {
		return new RewardGiver();
	}

}