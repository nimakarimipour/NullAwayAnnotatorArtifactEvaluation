class A {
    
    @Nullable Field f;

    Field getF(){
        return f;
    }
}

class B extends A{

    @Deprecated //Also no use in project.
    Field foo(){

        return getF();
    }
}



