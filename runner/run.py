import os
import json
import time


# Run with Python2
PROJECT_DIR = "/home/nima/Developer/AutoFixer/Evaluation/Projects/{}"
DISP = "{} & {} & {} & {}\n"
CONFIG = {
    "PROJECT_PATH": "/home/nima/Developer/AutoFixer/Evaluation/Projects/libgdx",
    "BUILD_COMMAND": "./gradlew gdx:build -x test",
    "ANNOTATION":{
        "INITIALIZE": "com.badlogic.gdx.Initializer",
        "NONNULL": "javax.annotation.NonNull",
        "NULLABLE": "javax.annotation.Nullable"
    },
    "FORMAT": False,
    "DEPTH": 0
}

with open('../projects.json') as f:
    projects = json.load(f)
    for project in projects['projects']:
        project['active'] = True
        if project['active']:
            COMMAND = "cd {} && {}".format(PROJECT_DIR.format(project['path']), {})
            os.system(COMMAND.format("git reset --hard"))
            os.system(COMMAND.format("git checkout docker"))
            os.system(COMMAND.format("git branch -D paper"))
            os.system(COMMAND.format("git checkout -b paper"))
            os.system(COMMAND.format(project['build']))
            before = len(open("/tmp/NullAwayFix/errors.csv",'r').readlines()) - 1
            config = CONFIG.copy()
            config['PROJECT_PATH'] = PROJECT_DIR.format(project['path'])
            config['BUILD_COMMAND'] = project['build']
            config['ANNOTATION']['INITIALIZE'] = project['annot']['init']
            config['ANNOTATION']['NULLABLE'] = project['annot']['nullable']
            with open('/home/nima/Developer/AutoFixer/Diagnoser/config.json', 'w') as outfile:
                json.dump(config, outfile)
            start_time = time.time()
            os.system("cd /home/nima/Developer/AutoFixer/Diagnoser/ && python3 run.py loop")
            total_time = time.time() - start_time
            os.system("mv /tmp/NullAwayFix/log.txt /tmp/NullAwayFix/{}.txt".format(project['name']))
            os.system(COMMAND.format(project['build']))
            after = len(open("/tmp/NullAwayFix/errors.csv",'r').readlines()) - 1
            file1 = open("ans.txt", "a")  # append mode
            file1.write(DISP.format(project['name'], before, after, int(total_time)))
            file1.close()