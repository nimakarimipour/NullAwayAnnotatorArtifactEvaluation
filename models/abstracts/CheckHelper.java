class Helper {
    
    static boolean check(NullableObject param){
        return param != null;
    }
}

class B{

    bar(@Nullable NullableObject param){
        if(Helper.check(param)){
            para.foo();
        }
    }
}
