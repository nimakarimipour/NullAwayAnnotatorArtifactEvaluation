//Reason for: A(@Nullable Field f);


class A {

    A(Field f){
        
    }
}

class B extends A{

    B(@Nullable Field f){
       super(f); //Here we make A to accept Nullable f
    }
}

class C extends B{
    B(){
        super(null); //Here we make A to accept Nullable f
     }
}
