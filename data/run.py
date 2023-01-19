import os
import json
import sys

PROJECT_DIR = "/Users/nima/Developer/NullAwayFixer/Projects/{}"
BRANCHES = {
    "nimak/pc",
    "nimak/p",
    "nimak/no-opt"
    # "nimak/exs",
}
DATA = {}


def execute(command):
    print("Executing: " + command, flush=True)
    sys.stdout.flush()
    os.system(command)


with open('../projects.json') as f:
    execute("cd /tmp && mkdir NullAwayFix")
    execute("cd /tmp/NullAwayFix && mkdir 0")
    execute("cp ~/Desktop/scanner.xml /tmp/NullAwayFix/scanner.xml")
    execute("cp ~/Desktop/nullaway.xml /tmp/NullAwayFix/nullaway.xml")
    projects = json.load(f)
    for project in projects['projects']:
        if project['name'] == 'SpringBoot':
            project_dir = PROJECT_DIR.format(project['path'])
            COMMAND = "cd {} && {}".format(PROJECT_DIR.format(project['path']), {})
            numbers = {}
            execute(COMMAND.format("git reset --hard"))
            execute(COMMAND.format("git pull"))
            execute(COMMAND.format("git checkout nimak/exs"))
            execute(COMMAND.format("git grep \"@Nullable\" > nullable_annot.txt"))
            after = len(open(project_dir + "/nullable_annot.txt", "r").readlines())
            execute(COMMAND.format("rm nullable_annot.txt"))
            execute(COMMAND.format("git reset --hard"))
            execute(COMMAND.format("git checkout nullaway"))
            execute(COMMAND.format("git grep \"@Nullable\" > nullable_annot.txt"))
            before = len(open(project_dir + "/nullable_annot.txt", "r").readlines())
            numbers['depth0'] = after - before

            execute(COMMAND.format("git checkout nimak/no-opt"))
            execute(COMMAND.format("git grep \"@Nullable\" > nullable_annot.txt"))
            after = len(open(project_dir + "/nullable_annot.txt", "r").readlines())
            execute(COMMAND.format("rm nullable_annot.txt"))
            execute(COMMAND.format("git reset --hard"))
            execute(COMMAND.format("git checkout nullaway"))
            execute(COMMAND.format("git grep \"@Nullable\" > nullable_annot.txt"))
            before = len(open(project_dir + "/nullable_annot.txt", "r").readlines())
            numbers['nullable'] = after - before

            execute(COMMAND.format("git reset --hard"))
            execute(COMMAND.format("git checkout nimak/nullunmarked"))
            execute(COMMAND.format("git grep \"@SuppressWarnings(\"NullAway\")\" > nullable_annot.txt"))
            after = len(open(project_dir + "/nullable_annot.txt", "r").readlines())
            execute(COMMAND.format("rm nullable_annot.txt"))
            execute(COMMAND.format("git reset --hard"))
            execute(COMMAND.format("git checkout nullaway"))
            execute(COMMAND.format("git grep \"@SuppressWarnings(\"NullAway\")\" > nullable_annot.txt"))
            before = len(open(project_dir + "/nullable_annot.txt", "r").readlines())
            numbers['suppress'] = after - before

            execute(COMMAND.format("git reset --hard"))
            execute(COMMAND.format("git checkout nimak/nullunmarked"))
            execute(COMMAND.format("git grep \"@SuppressWarnings(\"NullAway.Init\")\" > nullable_annot.txt"))
            after = len(open(project_dir + "/nullable_annot.txt", "r").readlines())
            execute(COMMAND.format("rm nullable_annot.txt"))
            execute(COMMAND.format("git reset --hard"))
            execute(COMMAND.format("git checkout nullaway"))
            execute(COMMAND.format("git grep \"@SuppressWarnings(\"NullAway.Init\")\" > nullable_annot.txt"))
            before = len(open(project_dir + "/nullable_annot.txt", "r").readlines())
            numbers['suppress_init'] = after - before

            execute(COMMAND.format("git reset --hard"))
            execute(COMMAND.format("git checkout nimak/nullunmarked"))
            execute(COMMAND.format("git grep \"@NullUnmarked\" > nullable_annot.txt"))
            after = len(open(project_dir + "/nullable_annot.txt", "r").readlines())
            execute(COMMAND.format("rm nullable_annot.txt"))
            execute(COMMAND.format("git reset --hard"))
            execute(COMMAND.format("git checkout nullaway"))
            execute(COMMAND.format("git grep \"@NullUnmarked\" > nullable_annot.txt"))
            before = len(open(project_dir + "/nullable_annot.txt", "r").readlines())
            numbers['nullunmarked'] = after - before

            DATA[project['name']] = numbers

json.dump(DATA, open('spring.json', 'w'))
