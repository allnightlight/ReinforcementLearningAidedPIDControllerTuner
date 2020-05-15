package framework;

public class EnvironmentFactory {
		
	public EnvironmentFactory() {
		// TODO Auto-generated constructor stub
	}
	
	public Environment create(BuildOrder buildOrder) {
		return new Environment();
	}

}