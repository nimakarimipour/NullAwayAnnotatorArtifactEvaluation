class A {

    @Nullable Field f;
}

class B {

    void foo(A a){
        if(a.f != null){
            bar(a);
        }
    }

    void bar(A a){
        a.bar();
    }
}
