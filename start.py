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
    # file_object = open('log.txt', 'a')
    # file_object.write("\n" + str(message))
    # file_object.close()

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


def prepare_project(project):
    log("Preparing project " + project['name'])
    change_dir = "cd " + PROJECTS_DIR
    if (not os.path.isdir(PROJECTS_DIR + project['name'] + "/")):
        log("Project does not exist, cloning now...")
        exec(change_dir + " && git clone " + project['git'].format(
            GIT_USERNAME, GIT_KEY))
    else:
        log("Project already exists")
    exec(change_dir + project['path'] + " && git reset --hard && git checkout gc_1 && git pull")
    exec(change_dir + project['path'] + " && git branch -d " + project['branch'])
    exec(change_dir + project['path'] + " && git push " + project['git'].format(
            GIT_USERNAME, GIT_KEY) + " --delete " + project['branch'])
    exec(change_dir + project['path'] + " && git checkout -b " + project['branch'])
    exec(change_dir + project['path'] + " && git push --set-upstream " + project['git'].format(
            GIT_USERNAME, GIT_KEY) + " " + project['branch'])
    exec("cd /tmp/Diagnoser/ && python3 run.py reset")

    log("Making the first build of the project")
    exec(change_dir + project['path'] + " && " + project['build'])
    log("Build finished.")
    log("Finished.")

def commit():
    log("trying to make a commit")
    exec("git pull")
    exec("git add .")
    exec("git commit -m \"changes comming from google cloud\"")
    exec("git push " +
              "https://{}:{}@github.com/nimakarimipour/Docker_AE_NA.git".
              format(GIT_USERNAME, GIT_KEY))


def autofix(project):
    log("Autofixing project: " + str(project['name']))
    log("Preparing config.json...")
    config = {
        "PROJECT_PATH": PROJECTS_DIR + project['path'],
        "BUILD_COMMAND": project['build'],
        "INITIALIZE_ANNOT": project['init_annot'],
        "FORMAT": project['format']
    }
    log("Prepared: " + str(config))
    with open('/tmp/Diagnoser/config.json', 'w') as outfile:
        json.dump(config, outfile)
        outfile.close()
    log("Finished writing.")
    if(project['preprocess']):
        log("Running autofix (pre)...")
        exec("cd /tmp/Diagnoser/ && python3 run.py pre")
        log("Running autofix (pre) finished")
    else:
        log("Skipping preproces...")
    log("Running autofix (loop)...")
    exec("cd /tmp/Diagnoser/ && python3 run.py loop")
    log("Running autofix (loop) finished")

    #todo change this in future.
    exec("cp -r /tmp/NullAwayFix/. " + PROJECTS_DIR + project['path'])

    change_path_to_project = "cd " + PROJECTS_DIR + project['path']
    exec(change_path_to_project + " && git add .")
    exec(change_path_to_project +
              " && git commit --no-verify -m \"final result of docker\"")
    exec(change_path_to_project + " && git push " + project['git'].format(GIT_USERNAME, GIT_KEY))
    log("Commited changes to project: " + project['name'])

    log("Copying infos in results directory.")
    exec("cd results/ && rm -rvf " + project['name'])
    exec("cd results/ && mkdir " + project['name'])
    exec("cp -r /tmp/NullAwayFix/. " + "results/" + project['name'])
    log("Copying finished.")

def run():
    with open('./projects.json') as f:
        projects = json.load(f)
        for project in projects['projects']:
            if project['active']:
                start = time.time()
                try:
                    prepare_project(project)
                    autofix(project)
                    log("successfully ran the command for project: " +
                        project['name'])
                except Exception:
                    log("something went wrong for: " + project['name'])
                finally:
                    end = time.time()
                    file_object = open(project['name'] + '.txt', 'a')
                    file_object.write("\n" + project['name'] + ": " + str(end - start))
                    file_object.close()
                    log("requesting commit")
                    commit()
                    log("finsihed commit")

prepare()
run()
