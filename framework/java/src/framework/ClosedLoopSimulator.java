package framework;

public class ClosedLoopSimulator {
	
	private Environment environment;
	private Agent agent;
	private ObservationSequence observationSequenceLast;
	private Action actionLast;
	private ObservationSequence observationSequencePrev;
	private int nSeq;
	
	public ClosedLoopSimulator(Environment environment, Agent agent, int nSeq) {
		// TODO Auto-generated constructor stub
		this.agent = agent;
		this.environment = environment;
		this.observationSequenceLast = new ObservationSequence();
		this.nSeq = nSeq;
		this.actionLast = null;
		this.observationSequencePrev = null;
	}
	
	public void init() {
		this.environment.init();
		this.observationSequenceLast.clear();
		this.observationSequencePrev = this.observationSequenceLast.copy();
		
		Observation observation = this.environment.observe();
		this.observationSequenceLast.add(observation);
	}
	
	public void update() {
		this.observationSequencePrev = this.observationSequenceLast.copy();
		
		this.actionLast = this.agent.call(this.observationSequenceLast);
		this.environment.update(this.actionLast);
		Observation observation = this.environment.observe();
		if (this.observationSequenceLast.size() >= this.nSeq) {
			this.observationSequenceLast.remove(0);			
		}
		this.observationSequenceLast.add(observation);		
	}
	
	public void requestInit(Trainer trainer) {
		init();
		trainer.addObservationSequence(this.observationSequenceLast.copy());
		trainer.setTimeLastUpdate(-1);
		trainer.setTimeSimulation(-1);
	}
	
	public void requestUpdate(Trainer trainer) {
		
		this.update();
		
		Reward rewardLast = trainer.reward(this.observationSequencePrev, this.actionLast);
				
		trainer.addObservationSequence(this.observationSequenceLast.copy());
		trainer.addAction(this.actionLast);
		trainer.addReward(rewardLast);
		trainer.addTimeSimulation();		
	}

}
