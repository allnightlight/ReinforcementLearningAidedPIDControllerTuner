package framework;

public class BuildOrder {
	
	private int nIteration;
	private int nSeq;
	private int nHorizonValueOptimization;
	private int nIntervalPolicyOptimization;
	private int nBatchPolicyOptimization;
	private int nSaveInterval;
	private String description;
	
	
	public BuildOrder(int nIteration, int nSeq, int nHorizonValueOptimization, int nIntervalPolicyOptimization, int nBatchPolicyOptimization, int nSaveInterval, String description) {
		// TODO Auto-generated constructor stub
		this.nIteration                  = nIteration;
		this.nSeq                        = nSeq;
		this.nHorizonValueOptimization   = nHorizonValueOptimization;
		this.nIntervalPolicyOptimization = nIntervalPolicyOptimization;
		this.nBatchPolicyOptimization    = nBatchPolicyOptimization;
		this.nSaveInterval 				 = nSaveInterval;
		this.description				 = description;
	}	
	
	public int getnIteration() {
		return nIteration;
	}
	
	public int getnSeq() {
		return nSeq;
	}
	
	public int getnHorizonValueOptimization() {
		return nHorizonValueOptimization;
	}
	
	public int getnIntervalPolicyOptimization() {
		return nIntervalPolicyOptimization;
	}
	
	public int getnBatchPolicyOptimization() {
		return nBatchPolicyOptimization;
	}
	
	public int getnSaveInterval() {
		return nSaveInterval;
	}
	
	public String getDescription() {
		return description;
	}
	
}
