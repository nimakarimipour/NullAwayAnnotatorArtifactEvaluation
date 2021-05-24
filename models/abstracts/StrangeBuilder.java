public class A {

    Field f1;
    Field f2;
    FIeld f3;

    A(){
        f1 = null;
        f2 = null;
        f3 = null;
    }

    A(Field f1, Field f2, FIeld f3){
        this.f1 = f1;
        this.f2 = f2;
        this.f3 = f3;
    }

    A initF1(Field f1){
        return new FIeld(f1, this.f2, this.f3);
    }

    A initF2(Field f2){
        return new FIeld(this.f1, f2, this.f3);
    }

    A initF3(Field f3){
        return new FIeld(this.f1, this.f2, f3);
    }
}
