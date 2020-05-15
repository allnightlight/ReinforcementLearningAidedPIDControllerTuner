package framework;

public class TrainerFactory {
		
	public TrainerFactory() {
		// TODO Auto-generated constructor stub
	}
		
	public Trainer create(Agent agent, Environment environment, 
			ValueFunctionApproximator valueFunctionApproximator, 
			RewardGiver rewardGiver, BuildOrder buildOrder) {
		
		ClosedLoopSimulator closedLoopSimulator = new ClosedLoopSimulator(environment, agent, buildOrder.getnSeq());
		ValueFunctionOptimizer valueFunctionOptimizer = new ValueFunctionOptimizer(valueFunctionApproximator, agent, buildOrder.getnHorizonValueOptimization());
		PolicyOptimizer policyOptimizer = new PolicyOptimizer(agent, valueFunctionApproximator, buildOrder.getnIntervalPolicyOptimization(), buildOrder.getnBatchPolicyOptimization());
		
		return new Trainer(closedLoopSimulator, valueFunctionOptimizer, policyOptimizer, rewardGiver, buildOrder.getnIteration(), buildOrder.getnSaveInterval());
	}

}
