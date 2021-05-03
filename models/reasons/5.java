//Reason for: @Nullabe Object foo();

class A{

    B b = new B();
    Object foo(){
        return b.bar();
    }
}

class B{

    Map map;

    @Nullabe
    Object foo(){
        if(m.isEmpty()){
            return null;
        }else{
            return m.get(0);
        }
    }
}