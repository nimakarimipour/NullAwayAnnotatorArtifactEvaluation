class A {

    //T is generic here
    T getT();
}

class B extends A{

    @Nullable
    Object getT(){
        return null;
    }
}