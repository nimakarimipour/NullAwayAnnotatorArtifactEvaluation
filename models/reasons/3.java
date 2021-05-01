class A {

    A(Field f){
        
    }
}

class B extends A{

    B(@Nullable Field f){
       super(f); //Here we make A to accept Nullable
    }
}
