package framework;

public class Utils {
	
	static String generateRandomString(int length) {
		// NOT IMPLEMENTED YET

		return "TestStringabcEFG123";
	}
	
	static public MyArray<Integer> myRandomRrandint(int nLow, int nHigh, int nSize) {
		
		// NOT IMPLEMENTED YET
		
		int j;
		MyArray<Integer> indexes = new MyArray<Integer>();
		for(int i=0;i < nSize; i ++) {
			j = i % (nHigh - nLow) + nLow;
			indexes.add(j);
		}
		
		return indexes;
	}
	
	static public String generateCurrentDatetimeAsString() {
		return "2020-05-05 14:48:01";
	}
	

}
