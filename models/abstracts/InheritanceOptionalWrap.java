interface A {
    foo();
}


class B implements A{

    @Nullable 
    foo(){

    }
}


class C {
    B b = new B();

    void bar(){
        return Optional.ofNullable(b.foo());
    }
}