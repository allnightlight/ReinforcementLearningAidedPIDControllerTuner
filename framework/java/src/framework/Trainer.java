package framework;

public class Trainer {
	
	
	private ClosedLoopSimulator closedLoopSimulator;
	private ValueFunctionOptimizer valueFunctionOptimizer;
	private PolicyOptimizer policyOptimizer;
	
	private int timeSimulation;
	private int timeLastUpdate;
	
	private MyArray<Action> historyActions;
	private MyArray<Reward> historyRewards;
	private MyArray<ObservationSequence> historyObservationSequences;
	
	private RewardGiver rewardGiver;
	
	private int nIteration;
	private int nSaveInterval;
		
	public Trainer(ClosedLoopSimulator closedLoopSimulator, ValueFunctionOptimizer valueFunctionOptimizer, PolicyOptimizer policyOptimizer, RewardGiver rewardGiver, int nIteration, int nSaveInterval) {
		// TODO Auto-generated constructor stub
		
		this.closedLoopSimulator = closedLoopSimulator;
		this.valueFunctionOptimizer = valueFunctionOptimizer;
		this.policyOptimizer = policyOptimizer;
		this.rewardGiver = rewardGiver;
		this.nIteration = nIteration;
		this.nSaveInterval = nSaveInterval;
		
		historyActions = new MyArray<Action>();
		historyObservationSequences = new MyArray<ObservationSequence>();
		historyRewards = new MyArray<Reward>();
		
	}
	
	public void init() {
		this.historyActions.clear();
		this.historyObservationSequences.clear();
		this.historyRewards.clear();		
		this.closedLoopSimulator.requestInit(this);
	}
	
	public void train(int nIterationLocal) {
		for(int i=0; i < nIterationLocal;i ++) {
			this.closedLoopSimulator.requestUpdate(this);
			this.valueFunctionOptimizer.requestUpdate(this);
			this.policyOptimizer.requestUpdate(this);
		}		
	}
	
	public void requestTrain(Builder builder) {
		this.init();
		int cnt = 0;
		while(true) {
			if(cnt < this.nIteration) {
				builder.saveAgent(this);		
				this.train(this.nSaveInterval);
				cnt += this.nSaveInterval;				
			}else {
				builder.saveAgent(this);
				break;
			}
		}
	}
	
	
	public void addObservationSequence(ObservationSequence observationSequence){
	    historyObservationSequences.add(observationSequence);
	}

	public void addAction(Action action){
	    historyActions.add(action);
	}

	public void addReward(Reward reward){
	    historyRewards.add(reward);
	}

	public ObservationSequence getObservationSequence(int idx){
	    return historyObservationSequences.get(idx);
	}

	public Action getAction(int idx){
	    return historyActions.get(idx);
	}

	public Reward getReward(int idx){
	    return historyRewards.get(idx);
	}

	public Reward reward(ObservationSequence observationSequence, Action action){
	    return rewardGiver.evaluate(observationSequence, action);
	}

	public void addTimeSimulation(){
		timeSimulation += 1;
	}

	public void markPolicyUpdate(){
	    timeLastUpdate = this.timeSimulation;
	}
	
	public int getTimeSimulation() {
		return timeSimulation;
	}
	public int getTimeLastUpdate() {
		return timeLastUpdate;
	}

	public void setTimeSimulation(int timeSimulation) {
		this.timeSimulation = timeSimulation;
	}

	public void setTimeLastUpdate(int timeLastUpdate) {
		this.timeLastUpdate = timeLastUpdate;
	}
	
	
}
