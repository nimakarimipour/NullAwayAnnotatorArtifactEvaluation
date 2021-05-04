abstract class A {
    Field f;

    foo(){
        f.bar();
    }
}

class B extends A {
    
    B(){
        f = new Field();
    }
}
