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
    log("Cloning project " + project['name'])
    change_dir = "cd " + PROJECTS_DIR
    if(not os.path.isdir(PROJECTS_DIR + project['name'] + "/")):
        command = change_dir + " && git clone " + project['git'].format(GIT_USERNAME, GIT_KEY) + " < git.key"
        print("Command: " + command)
        os.system(command)
    else:
        log("Project already exists")
    delete_file("/tmp/NullAwayFix/fixes.json")
    delete_file("/tmp/NullAwayFix/diagnose.json")
    delete_file("/tmp/NullAwayFix/diagnose_report.json")

def commit():
    log("trying to make a commit")
    os.system("git add .")
    os.system("git commit -m \"changes comming from docker\"")
    os.system("git push " + project['git'].format(GIT_USERNAME, GIT_KEY))


def make_report(project):
    log("trying to make a report for project: " + str(project['name']))

    change_dir = "cd " + PROJECTS_DIR
    change_dir += project['path'] + "/"
    log("changing branch: " + str(change_dir))
    os.system(change_dir + " && git reset --hard && git checkout diagnose && git reset --hard && git pull")
    log("finished setting the branch: " + str(change_dir))

    log("building project")
    os.system(change_dir + " && ./gradlew build")

    log("making diagnose.json")
    os.system("cp /tmp/NullAwayFix/fixes.json /tmp/NullAwayFix/diagnose.json")

    log("starting diagnose tasks")
    os.system(change_dir + " && ./gradlew diagnose")
    log("finished diagnose_report.json")

    log("copying to right results directory")
    os.system("cp /tmp/NullAwayFix/diagnose_report.json ./results/")
    os.system("mv ./results/diagnose_report.json ./results/" +
              project['name'] + ".json")

    log("finished make report request")

def run():
    with open('./projects.json') as f:
        projects = json.load(f)
        for project in projects['projects']:
            if project['active']:
                try:
                    prepare_project(project)
                    make_report(project)
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
