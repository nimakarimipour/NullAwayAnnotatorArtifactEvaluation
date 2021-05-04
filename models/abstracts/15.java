abstract class A {

    Field f;

    Field getF();

    boolean checkF();
}

abstract class B extends A {

    Field getF(){
        return f;
    }

    boolean checkF(){
        return f != null;
    }
}

class C{
    A a = new A();

    String foo(){
        if(checkF()){
            return getF().toString();
        }
    }
}
