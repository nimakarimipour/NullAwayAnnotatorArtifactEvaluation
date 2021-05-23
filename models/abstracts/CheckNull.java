class A{

    A(){
        Object object;
        boolean isNull = object == null;
        if(!isNull){
            object.foo();
        }
    }
}