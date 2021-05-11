class A{

    @Nullable Field f;
    int size;

    void bar(){
        if(size > 0){
            f.bar();
        }
    }
}