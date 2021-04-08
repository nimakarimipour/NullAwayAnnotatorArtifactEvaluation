import json
import os
import sys

PROJECTS_DIR = "/tmp/projects/"
GIT_USERNAME = str(sys.argv[1])
GIT_KEY = str(sys.argv[2])


def log(message):
    print("log: " + message)
    file_object = open('log.txt', 'a')
    file_object.write("\n" + str(message))
    file_object.close()


def delete_file(path):
    log("Cleaning: " + path)
    if os.path.exists(path):
        os.remove(path)
        log("Cleaned.")
    else:
        log("Does not exist.")


def prepare():
    try:
        os.makedirs(PROJECTS_DIR)
        os.makedirs("/tmp/NullAwayFix/")
    except FileExistsError:
        log("in prepare: project already exists")


def prepare_project(project):
    log("Preparing project " + project['name'])
    change_dir = "cd " + PROJECTS_DIR
    if (not os.path.isdir(PROJECTS_DIR + project['name'] + "/")):
        log("Project does not exist, cloning now...")
        command = change_dir + " && git clone " + project['git'].format(
            GIT_USERNAME, GIT_KEY)
        print("Command: " + command)
        os.system(command)
        print(change_dir + "/" + project['path'] + " && git checkout docker")
        os.system(change_dir + "/" + project['path'] +
                  " && git checkout docker")
    else:
        log("Project already exists")
        os.system(change_dir + "/" + project['path'] +
                  " && git reset --hard && git checkout docker && git pull")
        log("Finished git pull/reset")
    #todo use clean for script
    delete_file("/tmp/NullAwayFix/fixes.json")
    delete_file("/tmp/NullAwayFix/diagnose.json")
    delete_file("/tmp/NullAwayFix/diagnose_report.json")
    log("Preparing finished")


def commit():
    log("trying to make a commit")
    os.system("git pull")
    os.system("git add .")
    os.system("git commit -m \"changes comming from google cloud\"")
    os.system("git push " +
              "https://{}:{}@github.com/nimakarimipour/Docker_AE_NA.git".
              format(GIT_USERNAME, GIT_KEY))


def autofix(project):
    log("Autofixing project: " + str(project['name']))
    config = {
        "PROJECT_PATH": PROJECTS_DIR + project['path'],
        "BUILD_COMMAND": project['build'],
        "INITIALIZE_ANNOT": project['init_annot']
    }
    
    log("Finished make report request")


def run():
    with open('./projects.json') as f:
        projects = json.load(f)
        for project in projects['projects']:
            if project['active']:
                try:
                    prepare_project(project)
                    autofix(project)
                    log("successfully ran the command for project: " +
                        project['name'])
                except Exception:
                    log("something went wrong for: " + project['name'])
                finally:
                    log("requesting commit")
                    commit()
                    log("finsihed commit")


prepare()
run()
