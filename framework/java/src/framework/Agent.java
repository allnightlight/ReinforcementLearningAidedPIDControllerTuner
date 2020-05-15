package framework;

public class Agent {
	
	public AgentMemento createMemento() {
		return new AgentMemento();
	}
	public void loadFromMemento(AgentMemento agentMemento) {
		return;
	}
	
	public Action call(ObservationSequence observationSequence) {
		return new Action();
	}

}
