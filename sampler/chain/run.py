from distutils.command.clean import clean
import random
import json
import os
import platform
import re

# Run with Python2
PROJECT_DIR = "/home/nima/Developer/AutoFixer/Evaluation/Projects/{}" if platform.system(
) == "Linux" else "/Users/nima/Developer/NullAwayFixer/Projects/{}"
FIX_PATH = "/tmp/NullAwayFix/fixes.csv"


def readLines(path):
    f = open(path, 'r')
    lines = f.readlines()
    f.close()
    return lines


def convert_json_to_csv(name):
    f = open('./projects/{}/injected.json'.format(name))
    fixes = json.load(f)['fixes']
    f.close()
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
        lines.append(disp[:-3] + "\n")
    #todo for mac
    lines = [l.replace("$*$///home/nima/Developer/", "$*$file:///home/nima/Developer/", 1) for l in lines]
    f = open('./projects/{}/injected.csv'.format(name), "w")
    f.writelines(lines[:-1])
    f.close()


def clean_fix(fix):
    return fix[:fix.index("$*$true$*$null$*$null$*$") + len("$*$true")]


def remove_index_from_error(error):
    begin = error.index("(INDEX= ")
    end = begin + error[begin:].index(")")
    return error[:begin - 1] + error[end + 1:]


def remove_reason_field(path):
    fixes = readLines(path)
    lines = []
    for fix in fixes:
        vals = fix.split("$*$")
        disp = vals[0] + "$*$" + vals[1] + "$*$" + vals[2] + "$*$" + vals[
            3] + "$*$" + vals[4] + "$*$" + vals[
                5] + "$*$" + "null" + "$*$" + vals[7] + "$*$" + vals[
                    8] + "$*$" + vals[9] + "$*$" + vals[10] + "$*$" + vals[11]
        lines.append(str(disp))

    f = open(path, "w")
    f.writelines(lines)
    f.close()


def read_errors(path):
    lines = readLines(path)
    index = 0
    if (lines[len(lines) - 1] == '\n'):
        lines = lines[:-1]
    while (index < len(lines) and "error: [NullAway]" not in lines[index]):
        index += 1
    errors = []
    while (index < len(lines)):
        error = ""
        if ("error: [NullAway]" not in lines[index]):
            break
        while (index < len(lines)
               and "(see http://t.uber.com/nullaway )" not in lines[index]):
            error += lines[index]
            index += 1
        errors.append(error + "\t(see http://t.uber.com/nullaway )\n")
        index += 1
    return errors


def get_error_fix(path, command):
    os.system(command + " 2> errors.txt")
    remove_reason_field(FIX_PATH)
    fixes = readLines(FIX_PATH)
    return read_errors(path + "/errors.txt"), fixes[1:]


def exclude_fixes(target, toRemove):
    cleaned_target = [clean_fix(f) for f in toRemove]
    repeated = []
    for x in target:
        if clean_fix(x) in cleaned_target:
            print("Repeated: {}".format(clean_fix(x)))
            repeated.append(x)
    for fix in repeated:
        target = [t for t in target if t != fix]
    return target


def select_sample_errors(COMMAND, project):
    errors_before, _ = get_error_fix(PROJECT_DIR.format(project['path']),
                                     COMMAND.format(project['build']))

    os.system(COMMAND.format("git checkout final"))

    errors_after, _ = get_error_fix(PROJECT_DIR.format(project['path']),
                                    COMMAND.format(project['build']))

    errors_after = [remove_index_from_error(e) for e in errors_after]

    # remove repeated errors
    repeated = []
    for x in errors_before:
        if remove_index_from_error(x) in errors_after:
            repeated.append(x)
    for r in repeated:
        errors_before = [e for e in errors_before if e != r]

    selected = random.choices(errors_before, k=5)

    # Write selected errors
    file1 = open('projects/{}/selected.txt'.format(project['path']), 'w')
    file1.writelines(selected)
    file1.close()


def error_index(error):
    key = "[NullAway] (INDEX= "
    begin = error.index(key) + len(key)
    end = error[begin:].index(")") + begin
    return int(error[begin:end])


def fix_index(fix):
    vals = fix.split("$*$")
    return int(vals[len(vals) - 1])


def apply_fixes(fixes):
    ff = open(FIX_PATH, 'w')
    ff.writelines([str(f) for f in fixes])
    ff.close()
    os.system("java -jar injector.jar {}".format(FIX_PATH))


def get_corresponding_fixes(errors, fixes):
    indecies = [error_index(e) for e in errors]
    return [f for f in fixes if fix_index(f) in indecies]


def run():
    with open('../../projects.json') as f:
        projects = json.load(f)
        for project in projects['projects']:
            if project['active']:
                COMMAND = "cd {} && {}".format(
                    PROJECT_DIR.format(project['path']), {})

                convert_json_to_csv(project['path'])
                all_fixes = readLines('projects/{}/injected.csv'.format(
                    project['path']))
                
                # remove new lines from fixes
                all_fixes = [f[:-1] if f[len(f) - 1] == '\n' else f for f in all_fixes]

                # reset
                os.system(COMMAND.format("git reset --hard"))
                os.system(COMMAND.format("git checkout base"))

                # select new errors
                # select_sample_errors(COMMAND, project)

                # select sample errors with fixes
                selected = read_errors('projects/{}/selected.txt'.format(
                    project['path']))

                for i, error in enumerate(selected):
                    # reset
                    branch = "chain_{}".format(i)
                    os.system(COMMAND.format("git reset --hard"))
                    os.system(COMMAND.format("git checkout base"))
                    os.system(
                        COMMAND.format(
                            "git push origin --delete {}".format(branch)))
                    os.system(COMMAND.format(
                        "git branch -D {}".format(branch)))
                    os.system(
                        COMMAND.format("git checkout -b {}".format(branch)))

                    _, fixes = get_error_fix(
                        PROJECT_DIR.format(project['path']),
                        COMMAND.format(project['build']))

                    # inject the intial fix
                    init_fix = get_corresponding_fixes([error], fixes)
                    apply_fixes(init_fix)

                    while True:
                        error, new_fix_base = get_error_fix(
                            PROJECT_DIR.format(project['path']),
                            COMMAND.format(project['build']))

                        new_fix_base = exclude_fixes(new_fix_base, fixes)

                        to_apply = [
                            f for f in new_fix_base
                            if clean_fix(f) in all_fixes
                        ]

                        if (len(to_apply) == 0):
                            print("Finished.")
                            break
                        print("Going for another round...")
                        apply_fixes(to_apply)
                    
                    os.system(
                        COMMAND.format(
                            "git add . && git commit -m \"Chain Completed\" && git push --set-upstream origin {}".format(
                                branch)))


run()