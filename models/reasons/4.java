//Reason for: @Nullable Field f;


class A {

    Field f;
    Fielf others;

    A(){
        others = new Field();

        // Here we make f to be @Nullable; (Multiple Constructors)
    }

    A(){
        f = new Field();
    }
}
