package framework;

public class AgentFactory {
		
	public AgentFactory() {
		// TODO Auto-generated constructor stub
	}
	
	public Agent create(BuildOrder buildOrder) {
		return new Agent();
	}

}
