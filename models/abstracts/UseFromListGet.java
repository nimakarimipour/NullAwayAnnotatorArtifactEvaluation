import java.util.List;

public class A {

    @Nullable Field f;

    void setF(){
        f = new Field();
    }

    void releaseF(){
        f = null; //Here we set f to be Nullable
    }
}

class B{

    List list;

    void add(){
        A a = new A();
        a.setF();
        list.add(a);
    }

    void remove(){
        A a = list.get();
        Field localf = a.f;
        a.releaseF();
        localf.bar();
    }
}
