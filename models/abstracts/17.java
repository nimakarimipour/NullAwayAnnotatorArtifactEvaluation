class A {
    
    Field f;

    A(Field f){
        check(f);
        this.f = f;
    }

    void check(Field f){
        if(f == null){
            throw new IllegalArgumentException();
        }
    }
}
