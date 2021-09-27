import json
import os
import sys
import subprocess
import time

PROJECTS_DIR = "/tmp/projects/"
GIT_USERNAME = str(sys.argv[1])
GIT_KEY = str(sys.argv[2])


def log(message):
    print("log: " + message, flush=True)
    sys.stdout.flush()


def delete_file(path):
    log("Cleaning: " + path)
    if os.path.exists(path):
        os.remove(path)
        log("Cleaned.")
    else:
        log("Does not exist.")


def exec(command):
    print("Executing: " + command, flush=True)
    sys.stdout.flush()
    os.system(command)


def prepare():
    log("making directories.")
    dirs = [PROJECTS_DIR, "/tmp/NullAwayFix/", "./results"]
    for directory in dirs:
        try:
            os.makedirs(PROJECTS_DIR)
        except FileExistsError:
            log("in prepare: directory already exists: " + directory)


def make_branch(project, name):
    change_dir = "cd " + PROJECTS_DIR
    exec(change_dir + project['path'] +
         " && git reset --hard && git checkout docker && git pull")
    exec(change_dir + project['path'] + " && git branch -D " + name)
    exec(change_dir + project['path'] + " && git push " +
         project['git'].format(GIT_USERNAME, GIT_KEY) + " --delete " + name)
    exec(change_dir + project['path'] + " && git checkout -b " + name)
    exec(change_dir + project['path'] + " && git push --set-upstream " +
         project['git'].format(GIT_USERNAME, GIT_KEY) + " " + name)


def prepare_project(project, name):
    log("Preparing project " + project['name'])
    change_dir = "cd " + PROJECTS_DIR
    if (not os.path.isdir(PROJECTS_DIR + project['name'] + "/")):
        log("Project does not exist, cloning now...")
        exec(change_dir + " && git clone " +
             project['git'].format(GIT_USERNAME, GIT_KEY))
    else:
        log("Project already exists")
    make_branch(project, name)
    exec(change_dir + project['path'] + " && git branch")
    exec("cd /tmp/Diagnoser/ && python3 run.py reset")

    log("Making the first build of the project")
    exec(change_dir + project['path'] + " && " + project['build'])
    log("Build finished.")
    log("Finished.")


def commit():
    log("trying to make a commit")
    exec("git branch")
    exec("git pull")
    exec("git add .")
    exec("git commit -m \"changes comming from google cloud\"")
    exec("git push " +
         "https://{}:{}@github.com/nimakarimipour/Docker_AE_NA.git".format(
             GIT_USERNAME, GIT_KEY))


def autofix(project, depth):
    log("Autofixing project: " + str(project['name']))
    log("Preparing config.json...")
    config = {
        "PROJECT_PATH": PROJECTS_DIR + project['path'],
        "BUILD_COMMAND": project['build'],
        "ANNOTATION": {
            "INITIALIZE": project['annot']['init'],
            "NULLABLE": project['annot']['nullable'],
            "NONNULL": project['annot']['nonnull'],
        },
        "FORMAT": project['format'],
        "DEPTH": depth
    }
    log("Prepared: " + str(config))
    with open('/tmp/Diagnoser/config.json', 'w') as outfile:
        json.dump(config, outfile)
        outfile.close()
    log("Finished writing.")
    if (project['preprocess']):
        log("Running autofix (pre)...")
        exec("cd /tmp/Diagnoser/ && python3 run.py pre")
        log("Running autofix (pre) finished")
    else:
        log("Skipping preproces...")
    log("Running autofix (loop)...")
    exec("cd /tmp/Diagnoser/ && python3 run.py loop")
    log("Running autofix (loop) finished")

    change_path_to_project = "cd " + PROJECTS_DIR + project['path']
    exec(change_path_to_project + " && git branch")
    exec(change_path_to_project + " && git add .")
    exec(change_path_to_project +
         " && git commit --no-verify -m \"final result of docker\"")
    exec(change_path_to_project + " && git push " +
         project['git'].format(GIT_USERNAME, GIT_KEY))
    log("Commited changes to project: " + project['name'])

    log("Copying infos in results directory.")
    exec("cd results/ && rm -rvf " + project['name'])
    exec("cd results/ && mkdir " + project['name'])
    exec("mv /tmp/NullAwayFix/log.txt /tmp/NullAwayFix/log_{}.txt".format(
        depth))
    exec("cp -r /tmp/NullAwayFix/. " + "results/" + project['name'])
    log("Copying finished.")


def run():
    with open('./projects.json') as f:
        projects = json.load(f)
        for project in projects['projects']:
            if project['active']:
                for i in range(0, 11):
                    print("RUNNING FOR: " + str(project['name']) +
                          " at depth: " + str(i))
                    start = time.time()
                    prepare_project(project, "deep_" + str(i))
                    autofix(project, i)
                    log("successfully ran the command for project: " +
                        project['name'])
                    end = time.time()
                    time_json_file = open('time.json')
                    times = json.load(time_json_file)
                    time_json_file.close()
                    times[project['name']][i] = end - start
                    time_json_file = open('time.json', "w")
                    json.dump(times, time_json_file)
                    time_json_file.close()
                    log("requesting commit")
                    commit()
                    log("finsihed commit")


prepare()
run()