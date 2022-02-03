import random
import json
import os
import platform

# Run with Python2
PROJECT_DIR = "/home/nima/Developer/AutoFixer/Evaluation/Projects/{}" if platform.system(
) == "Linux" else "/Users/nima/Developer/NullAwayFixer/Projects/{}"
FIX_PATH = "/tmp/NullAwayFix/fixes.csv"


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
    remove_reason_field(FIX_PATH)
    fixes = open(FIX_PATH, 'r').readlines()
    return readErrors(path + "/errors.txt"), fixes[1:]


def exclude_list(target, toRemove):
    for x in target:
        if x in toRemove:
            target.remove(x)
    return target


def select_sample_errors(COMMAND, project):
    errors_before, fixes = get_error_fix(PROJECT_DIR.format(project['path']),
                                         COMMAND.format(project['build']))

    os.system(COMMAND.format("git checkout final"))

    errors_after, _ = get_error_fix(PROJECT_DIR.format(project['path']),
                                    COMMAND.format(project['build']))

    errors_before = exclude_list(errors_before, errors_after)
    selected = random.choices(errors_before, k=5)

    return selected, fixes


def error_index(error):
    key = "[NullAway] (INDEX= "
    begin = error.index(key) + len(key)
    end = error[begin:].index(")") + begin
    return int(error[begin:end])


def fix_index(fix):
    vals = fix.split("$*$")
    return int(vals[len(vals) - 1])


def apply_fixes(fixes):
    f = open(FIX_PATH, 'w')
    f.writelines(fixes)
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
                all_fixes = open('{}/injected.csv'.format(project['path']),
                                 'r').readlines()

                # reset
                os.system(COMMAND.format("git reset --hard"))
                os.system(COMMAND.format("git checkout base"))

                # select sample errors with fixes
                selected, fixes = select_sample_errors(COMMAND, project)

                # Write selected errors
                file1 = open('{}/selected.txt'.format(project['path']), 'w')
                file1.writelines(selected)
                file1.close()

                for i, error in enumerate(selected):
                    # reset
                    branch = "chain_{}".format(i)
                    os.system(COMMAND.format("git reset --hard"))
                    os.system(COMMAND.format("git checkout base"))
                    os.system(COMMAND.format(
                        "git branch -D {}".format(branch)))
                    os.system(
                        COMMAND.format("git checkout -b {}".format(branch)))

                    base, fixes = get_error_fix(
                        PROJECT_DIR.format(project['path']),
                        COMMAND.format(project['build']))

                    print("LENGTH : {}".format(len(fixes)))
                    print(fixes[0])

                    # inject the intial fix
                    init_fix = get_corresponding_fixes([error], fixes)
                    apply_fixes([init_fix])

                    while True:
                        new_base, fixes = get_error_fix(
                            PROJECT_DIR.format(project['path']),
                            COMMAND.format(project['build']))

                        new_fixes = get_corresponding_fixes(
                            exclude_list(new_base, base), fixes)
                        new_fixes = [f for f in new_fixes if f in all_fixes]

                        if (len(new_fixes) == 0):
                            break

                        apply_fixes(new_fixes)

                        base = new_base

                    os.system(
                        COMMAND.format(
                            "git push --set-upstream origin {}".format(
                                branch)))


run()