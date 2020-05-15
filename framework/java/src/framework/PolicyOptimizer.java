package framework;

public class PolicyOptimizer {
	
	private Agent agent;
	private ValueFunctionApproximator valueFunctionApproximator;	
	private int nIntervalPolicyOptimization;
	private int nBatchPolicyOptimization;
	
	public PolicyOptimizer(Agent agent, ValueFunctionApproximator valueFunctionApproximator, int nIntervalPolicyOptimization, int nBatchPolicyOptimization) {
		// TODO Auto-generated constructor stub
		this.agent = agent;
		this.valueFunctionApproximator = valueFunctionApproximator;
		this.nBatchPolicyOptimization = nBatchPolicyOptimization;
		this.nIntervalPolicyOptimization = nIntervalPolicyOptimization;
	}
	
	public void train(MyArray<ObservationSequence> observationSequences) {
		// NOT IMPLEMENTED YET
	}
	
	public void requestUpdate(Trainer trainer) {
		
		int nSample = 0;
		MyArray<ObservationSequence> observationSequences = null;
		if((trainer.getTimeSimulation()+1) % this.nIntervalPolicyOptimization == 0) {
			
			observationSequences = new MyArray<ObservationSequence>();
			nSample = trainer.getTimeSimulation() + 2;
			
			for(int i: Utils.myRandomRrandint(0, nSample, this.nBatchPolicyOptimization)) {
				observationSequences.add(trainer.getObservationSequence(i));
			}
			train(observationSequences);
			trainer.markPolicyUpdate();			
		}
	}
	
	
	
}
