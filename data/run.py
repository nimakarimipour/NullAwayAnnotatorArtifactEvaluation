import os
import json
import sys
import subprocess
import re

PROJECT_DIR = "/Users/nima/Developer/NullAwayFixer/Projects/{}"
CONFIG = json.load(open("annotator-config.json", 'r'))


def execute(command):
    print("Executing: " + command, flush=True)
    sys.stdout.flush()
    os.system(command)


def run_annotator(config, project_dir):
    execute("rm -rvf /tmp/NullAwayFix")
    outfile = open('/tmp/NullAwayAnnotator/runner/config.json', 'w')
    json.dump(config, outfile)
    outfile.close()
    execute("cd /tmp/NullAwayAnnotator/runner && ./start.sh --path /tmp/NullAwayAnnotator/runner/config.json")
    execute("cp -r /tmp/NullAwayFix {}/AnnotatorOut".format(project_dir))


def prepare(project, fresh=True):
    if fresh:
        delete_and_clone(project)
    execute("cd /tmp && mkdir NullAwayFix")
    execute("cd /tmp/NullAwayFix && mkdir 0")
    execute("cp ~/Desktop/config/scanner.xml /tmp/NullAwayFix/scanner.xml")
    execute("cp ~/Desktop/config/nullaway.xml /tmp/NullAwayFix/nullaway.xml")


def delete_and_clone(project):
    execute("rm -rvf {}".format(PROJECT_DIR.format(project['path'])))
    execute("cd {} && git clone git@github.com:nimakarimipour/{}.git".format(PROJECT_DIR.format(""), project['path']))


def get_active_projects():
    projects = json.load(open('projects.json', 'r'))
    return [project for project in projects['projects'] if project['name']=='WALA:UTIL']


def get_command_and_dir_for_project(project):
    project_dir = PROJECT_DIR.format(project['path'])
    command = "cd {} && {}".format(PROJECT_DIR.format(project['path']), {})
    return project_dir, command


def get_project_config(project_dir):
    return json.load(open("{}/annotator-config.json".format(project_dir)))


def read_from_log(project_dir, number):
    address = "{}/AnnotatorOut/log.txt".format(project_dir)
    if not os.path.exists(address):
        address = "{}/AnnotatorOut/NullAwayFix/log.txt".format(project_dir)
    lines = open(address, "r").readlines()
    return int(lines[number].split("=")[1])


def checkout(command, branch, fresh=False):
    if fresh:
        execute(command.format("git push origin --delete {}".format(branch)))
    execute(command.format("git reset --hard"))
    execute(command.format("git branch -D {}".format(branch)))
    execute(command.format("git reset --hard"))
    execute(command.format("git fetch"))
    execute(command.format("git pull"))
    execute(command.format("git checkout {}{}".format("-b " if fresh else "", branch)))


def make_new_config_for_project(project_dir):
    project_config = get_project_config(project_dir)
    config = CONFIG.copy()
    config['BUILD_COMMAND'] = project_config['BUILD_COMMAND']
    config['ANNOTATION']['INITIALIZER'] = project_config['ANNOTATION']['INITIALIZER']
    config['ANNOTATION']['NULLABLE'] = project_config['ANNOTATION']['NULLABLE']
    config['ANNOTATION']['NULL_UNMARKED'] = project_config['ANNOTATION']['NULL_UNMARKED']
    return config


def exhaustive_search():
    for project in get_active_projects():
        prepare(project)
        project_dir, command = get_command_and_dir_for_project(project)
        checkout(command, "nullaway")
        config = make_new_config_for_project(project_dir)
        config['DEPTH'] = 0
        checkout(command, "nimak/exs", fresh=True)
        run_annotator(config, project_dir)
        execute(command.format("git add ."))
        execute(command.format("git commit -m \"exhaustive_search\""))
        execute(command.format("git push --set-upstream origin {}".format("nimak/exs")))


def force_resolve():
    branches = ['nimak/exs', 'nullaway', 'nimak/p']
    for project in get_active_projects():
        prepare(project)
        project_dir, command = get_command_and_dir_for_project(project)
        for branch in branches:
            checkout(command, branch)
            config = make_new_config_for_project(project_dir)
            config['DEPTH'] = 0
            config['DISABLE_INFERENCE'] = 0
            checkout(command, branch + "-nullunmarked", fresh=True)
            run_annotator(config, project_dir)
            execute(command.format("git add ."))
            execute(command.format("git commit -m \"force resolve\""))
            execute(command.format("git push --set-upstream origin {}".format(branch + "-nullunmarked")))


def build(command, config):
    execute(command.format(config['BUILD_COMMAND'].split(" && ")[1]))


def unchecked():
    jar_path = '/Users/nima/.m2/repository/edu/ucr/cs/riple/clocunchecked/ClocUnchecked/0.0.1-SNAPSHOT/ClocUnchecked-0.0.1-SNAPSHOT.jar'
    data = {}
    branches = ['nimak/p-nullunmarked', 'nullaway-nullunmarked']
    for project in get_active_projects():
        project_data = {}
        prepare(project)
        project_dir, command = get_command_and_dir_for_project(project)
        for branch in branches:
            checkout(command, branch)
            result = subprocess.run(["java", "-jar", jar_path, "--path", project_dir],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            line = [l for l in result.stdout.splitlines() if l.startswith("Java")][0]
            numbers = re.findall(r'\d+', line)
            project_data[branch] = int(numbers[3]) - 2
        data[project['name']] = project_data
    json.dump(data, open('data/unchecked.json', 'w'))



def annotation_count():
    data = {}
    branches = ['nimak/p-new', 'nullaway', 'nimak/exs']
    for project in get_active_projects():
        prepare(project)
        project_dir, command = get_command_and_dir_for_project(project)
        data[project['name']] = {}
        for branch in branches:
            numbers = {}
            # @Nullable
            checkout(command, branch)
            execute(command.format("git grep \"@Nullable\" > nullable_annot.txt"))
            after = len(open(project_dir + "/nullable_annot.txt", "r").readlines())
            execute(command.format("rm nullable_annot.txt"))
            checkout(command, "nullaway")
            execute(command.format("git grep \"@Nullable\" > nullable_annot.txt"))
            before = len(open(project_dir + "/nullable_annot.txt", "r").readlines())
            numbers['nullable'] = after - before
            # @SuppressWarnings
            checkout(command, "{}-nullunmarked".format(branch))
            execute(command.format("git grep \"@SuppressWarnings(\\\"NullAway\\\")\" > nullable_annot.txt"))
            after = len(open(project_dir + "/nullable_annot.txt", "r").readlines())
            execute(command.format("rm nullable_annot.txt"))
            checkout(command, "nullaway")
            execute(command.format("git grep \"@SuppressWarnings(\\\"NullAway\\\")\" > nullable_annot.txt"))
            before = len(open(project_dir + "/nullable_annot.txt", "r").readlines())
            numbers['suppress'] = after - before
            # @SuppressWarnings Init
            checkout(command, "{}-nullunmarked".format(branch))
            execute(command.format("git grep \"@SuppressWarnings(\\\"NullAway.Init\\\")\" > nullable_annot.txt"))
            after = len(open(project_dir + "/nullable_annot.txt", "r").readlines())
            execute(command.format("rm nullable_annot.txt"))
            checkout(command, "nullaway")
            execute(command.format("git grep \"@SuppressWarnings(\\\"NullAway.Init\\\")\" > nullable_annot.txt"))
            before = len(open(project_dir + "/nullable_annot.txt", "r").readlines())
            numbers['suppress_init'] = after - before
            # @NullUnmarked
            checkout(command, "{}-nullunmarked".format(branch))
            execute(command.format("git grep \"@NullUnmarked\" > nullable_annot.txt"))
            after = len(open(project_dir + "/nullable_annot.txt", "r").readlines())
            execute(command.format("rm nullable_annot.txt"))
            checkout(command, "nullaway")
            execute(command.format("git grep \"@NullUnmarked\" > nullable_annot.txt"))
            before = len(open(project_dir + "/nullable_annot.txt", "r").readlines())
            numbers['nullunmarked'] = after - before
            print(numbers)
            data[project['name']][branch] = numbers
    json.dump(data, open('data/wala-annotation_count.json', 'w'))


def error_build_time_count():
    data = {}
    for project in get_active_projects():
        prepare(project)
        project_dir, command = get_command_and_dir_for_project(project)
        checkout(command, "nullaway")
        config = get_project_config(project_dir)
        branches = {
            "nimak/p",
            "nimak/no-opt",
            "nimak/p-1",
            "nimak/exs"
        }
        branches_data = {}
        for branch in branches:
            branch_data = {}
            checkout(command, branch)
            build(command, config)
            branch_data['error'] = len(open("/tmp/NullAwayFix/0/errors.tsv", "r").readlines()) - 1
            branch_data['time'] = read_from_log(project_dir, 3)
            branch_data['build'] = read_from_log(project_dir, 1)
            branches_data[branch] = branch_data
        data[project['name']] = branches_data
    json.dump(data, open('data/sp-build_error_time_count.json', 'w'))


annotation_count()
