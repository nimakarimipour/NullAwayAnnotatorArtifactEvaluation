//Reason for: @Nullable Field f; 

class A {

    Field f;

    A(boolean isOfTypeF){
        if(isOfTypeF){
            f = new Field();
        }
    }
}
