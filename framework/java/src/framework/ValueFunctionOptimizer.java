package framework;

public class ValueFunctionOptimizer {
	
	private ValueFunctionApproximator valueFunctionApproximator;
	private Agent agent;
	private int nHorizonValueOptimization;
	
	public ValueFunctionOptimizer(ValueFunctionApproximator valueFunctionApproximator, Agent agent, int nHorizonValueOptimization) {
		// TODO Auto-generated constructor stub
		this.valueFunctionApproximator = valueFunctionApproximator;
		this.agent = agent;
		this.nHorizonValueOptimization = nHorizonValueOptimization;
	}
	
	public void train(MyArray<ObservationSequence> observationSequences, MyArray<Action> actions, MyArray<Reward> rewards) {
		// NOT IMPLEMENTED YET
	}
	
	public void requestUpdate(Trainer trainer) {
		int timeLastUpdate = trainer.getTimeLastUpdate();
		int timeSimulation = trainer.getTimeSimulation();
		
		MyArray<ObservationSequence> observationSequences = null;
		MyArray<Action> actions = null;
		MyArray<Reward> rewards = null;
		int timeBegin = 0;
		int j = 0;
		
		if(timeLastUpdate + nHorizonValueOptimization <= timeSimulation) {
			observationSequences = new MyArray<ObservationSequence>();
			actions = new MyArray<Action>();
			rewards = new MyArray<Reward>();
			
			timeBegin = timeSimulation - this.nHorizonValueOptimization + 1;
			
			for(j = 0; j < this.nHorizonValueOptimization;j++) {
				observationSequences.add(trainer.getObservationSequence(timeBegin + j));
				actions.add(trainer.getAction(timeBegin + j));
				rewards.add(trainer.getReward(timeBegin + j));				
			}
			observationSequences.add(trainer.getObservationSequence(timeBegin + this.nHorizonValueOptimization));
			
			train(observationSequences, actions, rewards);        	
        }
	}
	
}
