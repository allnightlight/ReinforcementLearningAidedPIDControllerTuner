package framework;

public class ObservationSequence extends MyArray<Observation>{
	
	public ObservationSequence copy() {
		return (ObservationSequence)this.clone();
	}

}
