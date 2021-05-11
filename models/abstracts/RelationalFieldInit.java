public class A {

    Field f, other;

    A(){
        init(other);
        f = (other != null) ? new Field() : null;
    }

    foo(A a){
        if(a.other != null){
            a.f.bar();
        }
    }
}
