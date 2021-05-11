class A {

    @Nullable Field nullableField;
}

class B {

    void foo(A a){
        if(a.nullableField != null){
            bar(a);
        }
    }

    void bar(A a){
        a.nullableField.foo();
    }
}
