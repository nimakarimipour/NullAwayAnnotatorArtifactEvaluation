class A {

    Field f;

    Field GetterAndSetter(){
        //No other use of f in A
    }
}

class B extends A{

    init(){
        f = new Field();
    }
    //Many use of f without null check
}

// Another Example
// abstract class A {
//     Field f;

//     foo(){
//         f.bar();
//     }
// }

// class B extends A {
    
//     B(){
//         f = new Field();
//     }
// }
