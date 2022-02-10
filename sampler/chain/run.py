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


def checkout_to_branch(COMMAND, project, name, saveState=False):
    os.system("rm {}/errors.txt".format(PROJECT_DIR.format(project['path'])))
    if (saveState):
        os.system(COMMAND.format("git push origin --delete {}".format(name)))
        os.system(COMMAND.format("git branch -D {}".format(name)))
        os.system(COMMAND.format("git checkout -b {}"))
        os.system(COMMAND.format("git add ."))
        os.system(COMMAND.format("git commit -m \"Final Result\""))
        os.system(COMMAND.format("git push --set-upstream origin {}".format(name)))
    else:
        os.system(COMMAND.format("git reset --hard"))
        os.system(COMMAND.format("git checkout {}".format(name)))

def read_lines(path):
    f = open(path, 'r')
    lines = f.readlines()
    f.close()
    return lines


def run_autofix(project):
    os.system("rm /tmp/NullAwayFix/injected.json")
    CONFIG = {
        "PROJECT_PATH": "",
        "BUILD_COMMAND": "",
        "ANNOTATION": {
            "INITIALIZE": "",
            "NONNULL": "",
            "NULLABLE": ""
        },
        "FORMAT": False,
        "DEPTH": 4
    }
    config = CONFIG.copy()
    config['PROJECT_PATH'] = PROJECT_DIR.format(project['path'])
    config['BUILD_COMMAND'] = project['build']
    config['ANNOTATION']['INITIALIZE'] = project['annot']['init']
    config['ANNOTATION']['NULLABLE'] = project['annot']['nullable']
    with open(
            '/Users/nima/Developer/NullAwayFixer/Scripts/Diagnoser/config.json',
            'w') as outfile:
        json.dump(config, outfile)
    os.system(
        "cd /Users/nima/Developer/NullAwayFixer/Scripts/Diagnoser/ && python3 run.py loop"
    )


def copy_correct_nullaway_config(project):
    CONFIG = {
        "INHERITANCE_CHECK_DISABLED": False,
        "ANNOTATION": {
            "NONNULL": "UKNOWN",
            "NULLABLE": "UKNOWN"
        },
        "MAKE_CALL_GRAPH": False,
        "METHOD_PARAM_TEST": {
            "ACTIVE": False,
            "INDEX": 10000
        },
        "MAKE_METHOD_INHERITANCE_TREE": False,
        "LOG_ERROR": {
            "DEEP": False,
            "ACTIVE": True
        },
        "WORK_LIST": "*",
        "MAKE_FIELD_GRAPH": True,
        "SUGGEST": {
            "DEEP": False,
            "ACTIVE": True
        },
        "OPTIMIZED": False
    }
    config = CONFIG.copy()
    config['ANNOTATION']['NULLABLE'] = project['annot']['nullable']
    with open('/tmp/NullAwayFix/explorer.config', 'w') as outfile:
        json.dump(config, outfile)


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
    fixed = []
    for l in lines:
        index = [i.start() for i in re.finditer("\$\*\$", l)][4] + 3
        l = l[:index] + 'file:' + l[index:]
        fixed.append(l)

    f = open('./projects/{}/injected.csv'.format(name), "w")
    f.writelines(fixed)
    f.close()


def clean_fix(fix):
    return fix[:fix.index("$*$true$*$null$*$null$*$") + len("$*$true")]


def remove_index_from_error(error):
    begin = error.index("(INDEX= ")
    end = begin + error[begin:].index(")")
    return error[:begin - 1] + error[end + 1:]


def remove_reason_field(path):
    fixes = read_lines(path)
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
    lines = read_lines(path)
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
    fixes = read_lines(FIX_PATH)
    return read_errors(path + "/errors.txt"), fixes[1:]


def exclude_fixes(target, toRemove):
    cleaned_target = [clean_fix(f) for f in toRemove]
    repeated = []
    for x in target:
        if clean_fix(x) in cleaned_target:
            repeated.append(x)
    for fix in repeated:
        target = [t for t in target if t != fix]
    return target


def select_sample_errors(COMMAND, project):
    errors_before, _ = get_error_fix(PROJECT_DIR.format(project['path']),
                                     COMMAND.format(project['build']))

    checkout_to_branch(COMMAND, project, "final")

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

                if not os.path.exists("./projects/{}".format(project['path'])):
                    os.makedirs("./projects/{}".format(project['path']))

                # reset
                checkout_to_branch(COMMAND, project, "base")

                # get all fixes
                run_autofix(project)
                os.system(
                    "mv /tmp/NullAwayFix/injected.json ./projects/{}/injected.json"
                    .format(project['path']))
                convert_json_to_csv(project['path'])
                all_fixes = read_lines('projects/{}/injected.csv'.format(
                    project['path']))

                # push everythig to final branch
                checkout_to_branch(COMMAND, project, "final", saveState=True)

                # remove new lines from fixes
                all_fixes = [
                    f[:-1] if f[len(f) - 1] == '\n' else f for f in all_fixes
                ]

                # reset
                checkout_to_branch(COMMAND, project, "base")

                # copy the correct nullaway config
                copy_correct_nullaway_config(project)

                # select new sample errors
                select_sample_errors(COMMAND, project)

                # read sample errors
                selected = read_errors('projects/{}/selected.txt'.format(
                    project['path']))

                for i, error in enumerate(selected):
                    # reset
                    checkout_to_branch(COMMAND, project, "base")
                
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

                    checkout_to_branch(COMMAND, project, "chain_{}".format(i), saveState=True)


run()