class A {
    
    get(Foo foo){
        switch(foo.type){
            case "A":
                return new NonnullA();
            case "B":
                return new NonNullB();
            case "C":
                return null;
        }
    }

    void bar(){
        Foo foo = new Foo();
        foo.type = "A";
        get(foo).execute();
    }
}
