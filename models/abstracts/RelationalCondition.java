class A {
    
    @Nullable Field f;

    void foo(){
        if(exp_1){ //if exp_2 is false -> exp_1 => false
            if(exp_2){
                f = null;
            }else{
                f.bar();
            }
        }
    }
}
