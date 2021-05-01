public class A {

    public Object foo(){
        if(exp){
            return null; //here we annotate the method with @Nullable annotation.
        }
        return new Object();
    }
    
}
