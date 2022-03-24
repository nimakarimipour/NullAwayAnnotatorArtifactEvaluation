import glob
import os

root_dir = "/home/nima/Developer/AutoFixer/Evaluation/Projects/zuul/zuul-core/src/main/java"
for path in glob.iglob(root_dir + '**/**', recursive=True):
     if(os.path.isfile(path)):
         with open(path) as f:
            lines = f.readlines()
            for l in lines:
                if("org.checkerframework.checker.nullness.qual.Nullable" in l):
                    print(path)
