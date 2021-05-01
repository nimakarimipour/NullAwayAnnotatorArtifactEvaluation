package models.abstracts;

interface A {
    
    Object get();
}

class B implements A {
    
    @Nullable
    Object get(){
        if(exp){
            return null;
        }
        return new Object();
    }
}

class C {
    A a;

    C(A a){
        this.a = a;
    }

    foo(){
        Object a = a.get();
        // Use a with no if check...
    }
}