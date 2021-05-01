class A{
    @Nullable Field f;

    private LambdaClass f = new LambdaClass() {
        @Override
        public void foo() {
            //derefrence f here;
        }
    }
}

// If check for "f" observed in code