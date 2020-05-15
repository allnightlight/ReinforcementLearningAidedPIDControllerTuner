package framework;

public class StoreField {
	
	private int timeSimulation;
	private AgentMemento agentMemento;
	private BuildOrder buildOrder;
	private String timeStamp;
	
	public StoreField(int timeSimulation, AgentMemento agentMemento, BuildOrder buildOrder, String timeStamp) {
		// TODO Auto-generated constructor stub
		this.timeSimulation = timeSimulation;
		this.agentMemento = agentMemento;
		this.buildOrder = buildOrder;
		this.timeStamp = timeStamp;
	}
	
	public AgentMemento getAgentMemento() {
		return agentMemento;
	}
	
	public int getTimeSimulation() {
		return timeSimulation;
	}
	
	public BuildOrder getBuildOrder() {
		return buildOrder;
	}
	
	public String getTimeStamp() {
		return timeStamp;
	}
}
