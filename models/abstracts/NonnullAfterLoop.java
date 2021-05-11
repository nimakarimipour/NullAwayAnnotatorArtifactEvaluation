class A {


    Object get(){
        Object a = null;

        for(...){
            if(a == null){
                a = nonnullMethodReturnCall()
            }else{
                a = a.anotherNonnullMethodReturnCall();
            }
        }
        //Here we can add cast to Nonnull
        return a;
    }
}
