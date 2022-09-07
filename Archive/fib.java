public class fib{
   public static int recur(int n) {
      if ((n == 0) || (n == 1))
         return n;
      else {
          try {
  		        return recur(n-1) + recur(n-2);
 		    } catch(Exception e) {
 		        System.out.println("Exception: " + e);
 		        return -1;
 		    }
       }
   }
	public static void main(String args[]) {
	    while(true) {
	        try {
  			    recur(10000);
 		    } catch(Exception e) {
 		        System.out.println("Exception: " + e);
 		    }
 		}
	}
}