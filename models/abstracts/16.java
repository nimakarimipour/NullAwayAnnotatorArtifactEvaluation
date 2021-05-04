class A {
    
    Field b; // can be either b1, b2, b3

    boolean check() {
        // checks a state of A
        return false;
    }

    String bar(){
        if(b.equals("b1")){
            return "b1";
        } else if(b.equals("b2")){
            return "b2";
        } else if(b.equals("b3")){
            return "b3";
        }
        return null;
    }
}

class B {

    String buggy() {
        A a = new A();
        return a.bar().toString();
    }

    String correct(){
        A a = new A();
        //some constructions
        if(a.check()){
            return a.bar().toString();
        }
        return null;
    }
}
