class A {
    
    void bar(int i, int j){
        Foo f = (i < j) ? new Foo() : null;
        String name = (i < j) ? "Name" : null;

        bar(f, name);
    }

    void bar(Foo f, String name){
        if(name != null){
            f.bar();
        }
    }
}
