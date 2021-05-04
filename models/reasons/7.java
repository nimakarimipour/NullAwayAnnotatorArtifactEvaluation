//Reason for: @Nullable Field f;

class A {

    Field f;

    A(){
        f = new Field();
    }

    void onFinish(){
        f = null;
    }
    
}
