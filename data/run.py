import os
import json
import sys

PROJECT_DIR = "/Users/nima/Developer/NullAwayFixer/Projects/{}"


def execute(command):
    print("Executing: " + command, flush=True)
    sys.stdout.flush()
    os.system(command)


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
    return [project for project in projects['projects'] if project['active']]


def get_command_and_dir_for_project(project):
    project_dir = PROJECT_DIR.format(project['path'])
    command = "cd {} && {}".format(PROJECT_DIR.format(project['path']), {})
    return project_dir, command


def get_config(project_dir):
    return json.load(open("{}/annotator-config.json".format(project_dir)))


def read_from_log(project_dir, number):
    lines = open("{}/AnnotatorOut/log.txt".format(project_dir), "r").readlines()
    return int(lines[number].split("=")[1])


def checkout(command, branch):
    execute(command.format("git reset --hard"))
    execute(command.format("git checkout nullaway"))
    execute(command.format("git branch -D {}".format(branch)))
    execute(command.format("git reset --hard"))
    execute(command.format("git fetch"))
    execute(command.format("git pull"))
    execute(command.format("git checkout {}".format(branch)))


def build(command, config):
    execute(command.format(config['BUILD_COMMAND'].split(" && ")[1]))


def annotation_count():
    data = {}
    for project in get_active_projects():
        prepare(project)
        project_dir, command = get_command_and_dir_for_project(project)
        numbers = {}
        # @Nullable
        checkout(command, "nimak/p")
        execute(command.format("git grep \"@Nullable\" > nullable_annot.txt"))
        after = len(open(project_dir + "/nullable_annot.txt", "r").readlines())
        execute(command.format("rm nullable_annot.txt"))
        checkout(command, "nullaway")
        execute(command.format("git grep \"@Nullable\" > nullable_annot.txt"))
        before = len(open(project_dir + "/nullable_annot.txt", "r").readlines())
        numbers['nullable'] = after - before
        # @SuppressWarnings
        checkout(command, "nimak/nullunmarked")
        execute(command.format("git grep \"@SuppressWarnings(\\\"NullAway\\\")\" > nullable_annot.txt"))
        after = len(open(project_dir + "/nullable_annot.txt", "r").readlines())
        execute(command.format("rm nullable_annot.txt"))
        checkout(command, "nullaway")
        execute(command.format("git grep \"@SuppressWarnings(\\\"NullAway\\\")\" > nullable_annot.txt"))
        before = len(open(project_dir + "/nullable_annot.txt", "r").readlines())
        numbers['suppress'] = after - before
        # @SuppressWarnings Init
        checkout(command, "nimak/nullunmarked")
        execute(command.format("git grep \"@SuppressWarnings(\\\"NullAway.Init\\\")\" > nullable_annot.txt"))
        after = len(open(project_dir + "/nullable_annot.txt", "r").readlines())
        execute(command.format("rm nullable_annot.txt"))
        checkout(command, "nullaway")
        execute(command.format("git grep \"@SuppressWarnings(\\\"NullAway.Init\\\")\" > nullable_annot.txt"))
        before = len(open(project_dir + "/nullable_annot.txt", "r").readlines())
        numbers['suppress_init'] = after - before
        # @NullUnmarked
        checkout(command, "nimak/nullunmarked")
        execute(command.format("git grep \"@NullUnmarked\" > nullable_annot.txt"))
        after = len(open(project_dir + "/nullable_annot.txt", "r").readlines())
        execute(command.format("rm nullable_annot.txt"))
        checkout(command, "nullaway")
        execute(command.format("git grep \"@NullUnmarked\" > nullable_annot.txt"))
        before = len(open(project_dir + "/nullable_annot.txt", "r").readlines())
        numbers['nullunmarked'] = after - before
        data[project['name']] = numbers
    json.dump(data, open('annotation_count.json', 'w'))


def error_build_time_count():
    data = {}
    for project in get_active_projects():
        prepare(project)
        project_dir, command = get_command_and_dir_for_project(project)
        checkout(command, "nullaway")
        config = get_config(project_dir)
        branches = {
            "nimak/pc",
            "nimak/p",
            "nimak/no-opt"
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
    json.dump(data, open('data/build_error_time_count.json', 'w'))
