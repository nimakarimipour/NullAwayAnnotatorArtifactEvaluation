from dis import dis
import imp

import random
import json
import os
import re

# Run with Python2
PROJECT_DIR = "/Users/nima/Developer/NullAwayFixer/Projects/{}"
DISP = "{} & {} & {} & {}\n"
CONFIG = {
    "PROJECT_PATH": "/Users/nima/Developer/NullAwayFixer/Projects/libgdx",
    "BUILD_COMMAND": "./gradlew gdx:build -x test",
    "ANNOTATION": {
        "INITIALIZE": "com.badlogic.gdx.Initializer",
        "NONNULL": "javax.annotation.NonNull",
        "NULLABLE": "javax.annotation.Nullable"
    },
    "FORMAT": False,
    "DEPTH": 0
}


def convert_json_to_csv(name):
    f = open('./{}/injected.json'.format(name))
    fixes = json.load(f)['fixes']
    keys = "location$*$class$*$method$*$param$*$index$*$uri$*$reason$*$annotation$*$inject".split(
        "$*$")
    lines = []
    for fix in fixes:
        disp = ""
        for key in keys:
            if (key in fix.keys()):
                val = fix[key]
                disp += (val if val != None else "null") + "$*$"
            else:
                disp += "null" + "$*$"
        print(disp)
        lines.append(disp[:-3] + "\n")
    f = open('./{}/injected.csv'.format(name), "w")
    f.writelines(lines[:-1])
    f.close()


def remove_reason_field(path):
    fixes = open(path, 'r').readlines()
    lines = []
    for fix in fixes:
        vals = fix.split("$*$")
        disp = vals[0] + "$*$" + vals[1] + "$*$" + vals[2] + "$*$" + vals[
            3] + "$*$" + vals[4] + "$*$" + vals[
                5] + "$*$" + "null" + "$*$" + vals[7] + "$*$" + vals[
                    8] + "$*$" + vals[9]
        lines.append(disp + "\n")

    f = open(path, "w")
    f.writelines(lines)
    f.close()

def readErrors(path):
    lines = open(path, 'r').readlines()
    index = 0
    while ("error: [NullAway]" not in lines[index]):
        index += 1
    print(index)
    errors = []
    while (index < len(lines)):
        error = ""
        if ("error: [NullAway]" not in lines[index]):
            break
        while ("(see http://t.uber.com/nullaway )" not in lines[index]):
            error += lines[index]
            index += 1
        errors.append(error)
        index += 1
    return errors


def get_error_fix(path, command):
    os.system(command + " 2> errors.txt")
    remove_reason_field("/tmp/NullAwayFix/fixes.csv")
    fixes = open("/tmp/NullAwayFix/fixes.csv", 'r').readlines()
    return readErrors(path + "/errors.txt"), fixes


def select_sample_errors(COMMAND, project):
    os.system(COMMAND.format("git reset --hard"))
    os.system(COMMAND.format("git checkout base"))

    errors_before, fixes = get_error_fix(PROJECT_DIR.format(project['path']),
                                         COMMAND.format(project['build']))

    os.system(COMMAND.format("git checkout final"))

    errors_after, _ = get_error_fix(PROJECT_DIR.format(project['path']),
                                    COMMAND.format(project['build']))

    for x in errors_before:
        if x in errors_after:
            errors_before.remove(x)
    selected = random.choices(errors_before, k=5)
    return selected, fixes


def run():
    with open('../projects.json') as f:
        projects = json.load(f)
        for project in projects['projects']:
            project['active'] = True
            if project['active']:
                COMMAND = "cd {} && {}".format(
                    PROJECT_DIR.format(project['path']), {})

                # select sample errors with fixes
                selected, fixes = select_sample_errors(COMMAND, project)

                # Write selected errors
                file1 = open('{}/selected.txt'.format(project['path']), 'w')
                file1.writelines(selected)
                file1.close()


remove_reason_field("/tmp/NullAwayFix/fixes.csv")