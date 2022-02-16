import random
import json
import os
import platform
import re

# Run with Python2
PROJECT_DIR = "/home/nima/Developer/AutoFixer/Evaluation/Projects/{}" if platform.system(
) == "Linux" else "/Users/nima/Developer/NullAwayFixer/Projects/{}"
AUTO_FIXER_PATH = "/home/nima/Developer/AutoFixer/Diagnoser" if platform.system(
) == "Linux" else "/Users/nima/Developer/NullAwayFixer/Scripts/Diagnoser"
FIX_PATH = "/tmp/NullAwayFix/fixes.csv"


def checkout_to_branch(command, project, name, save_state=False):
    os.system("rm {}/errors.txt".format(PROJECT_DIR.format(project['path'])))
    if save_state:
        os.system(command.format("git push origin --delete {}".format(name)))
        os.system(command.format("git branch -D {}".format(name)))
        os.system(command.format("git checkout -b {}".format(name)))
        os.system(command.format("git add ."))
        os.system(command.format("git commit -m \"Final Result\""))
        os.system(
            command.format("git push --set-upstream origin {}".format(name)))
    else:
        os.system(command.format("git reset --hard"))
        os.system(command.format("git pull"))
        os.system(command.format("git checkout {}".format(name)))


def read_lines(path):
    f = open(path, 'r')
    lines = f.readlines()
    f.close()
    return [l[:-1] if l[len(l) - 1] == '\n' else l for l in lines]


def write_lines(path, lines):
    f = open(path, "w")
    f.writelines(lines)
    f.flush()
    f.close()


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
    with open('{}/config.json'.format(AUTO_FIXER_PATH), 'w') as outfile:
        json.dump(config, outfile)
    os.system("cd {} && python3 run.py loop".format(AUTO_FIXER_PATH))


def copy_correct_nullaway_config(project):
    CONFIG = {
        "INHERITANCE_CHECK_DISABLED": False,
        "ANNOTATION": {
            "NONNULL": "UNKNOWN",
            "NULLABLE": "UNKNOWN"
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
        display = ""
        for key in keys:
            if key in fix.keys():
                val = fix[key]
                display += (val if val is not None else "null") + "$*$"
            else:
                display += "null" + "$*$"
        lines.append(display[:-3] + "\n")
    fixed = []
    for l in lines:
        index = [i.start() for i in re.finditer("\$\*\$", l)][4] + 3
        to_add = 'file:' if l[index + 2] == "/" else "file:/"
        l = l[:index] + to_add + l[index:]
        fixed.append(l)

    write_lines('./projects/{}/injected.csv'.format(name), fixed)


def clean_fix(fix):
    return fix[:fix.index("$*$true$*$null$*$null$*$") + len("$*$true")]


def remove_index_from_error(error):
    begin = error.index("(INDEX= ")
    end = begin + error[begin:].index(")")
    return error[:begin - 1] + error[end + 1:]


def remove_line_number_from_error(error):
    begin = error.index(".java:") + len(".java")
    end = error.index(": error: [NullAway]")
    return int(error[begin + 1:end]), (error[:begin - 1] + error[end + 1:])


def remove_reason_field(path):
    fixes = read_lines(path)
    lines = []
    for fix in fixes:
        vals = fix.split("$*$")
        disp = vals[0] + "$*$" + vals[1] + "$*$" + vals[2] + "$*$" + vals[
            3] + "$*$" + vals[4] + "$*$" + vals[
                5] + "$*$" + "null" + "$*$" + vals[7] + "$*$" + vals[
                    8] + "$*$" + vals[9] + "$*$" + vals[10] + "$*$" + vals[11]
        lines.append(str(disp) + "\n")

    write_lines(path, lines)


def read_errors(path):
    lines = read_lines(path)
    index = 0
    if lines[len(lines) - 1] == '\n':
        lines = lines[:-1]
    while index < len(lines) and "error: [NullAway]" not in lines[index]:
        index += 1
    errors = []
    while index < len(lines):
        error = ""
        while index < len(lines) and "error: [NullAway]" not in lines[index]:
            index += 1
        while (index < len(lines)
               and "(see http://t.uber.com/nullaway )" not in lines[index]):
            error += lines[index]
            index += 1
        if error != "":
            errors.append(error + "\t(see http://t.uber.com/nullaway )\n")
        index += 1
    return errors


def get_error_fix(path, command):
    os.system(command + " 2> errors.txt")
    remove_reason_field(FIX_PATH)
    fixes = read_lines(FIX_PATH)
    return read_errors(path + "/errors.txt"), fixes[1:]


def exclude_fixes(target, to_remove):
    cleaned_to_remove = [clean_fix(f) for f in to_remove]
    cleaned_target = [clean_fix(f) for f in target]
    for f in cleaned_to_remove:
        if f in cleaned_target:
            cleaned_target.remove(f)
    return cleaned_target


def collection_contains_error(target, errors):
    number, target = remove_line_number_from_error(target)
    for error in errors:
        n, e = remove_line_number_from_error(error)
        if e == target and abs(number - n) < 10:
            return True
    return False


def select_sample_errors(command, project):
    checkout_to_branch(command, project, "base")
    errors_before, _ = get_error_fix(PROJECT_DIR.format(project['path']),
                                     command.format(project['build']))
    checkout_to_branch(command, project, "final")
    errors_after, _ = get_error_fix(PROJECT_DIR.format(project['path']),
                                    command.format(project['build']))
    print(
        "Number of errors at branch: {} is {}, and at branch: {} is {}".format(
            "base", len(errors_before), "final", len(errors_after)))

    # write before/after errors
    write_lines('projects/{}/before.txt'.format(project['path']),
                errors_before)
    write_lines('projects/{}/after.txt'.format(project['path']), errors_after)

    errors_after = [remove_index_from_error(e) for e in errors_after]

    # remove repeated errors
    repeated = []
    for x in errors_before:
        if collection_contains_error(x, errors_after):
            repeated.append(x)
    for r in repeated:
        errors_before = [e for e in errors_before if e != r]

    selected = random.choices(errors_before, k=min([5, len(errors_before)]))

    # Write selected errors
    write_lines('projects/{}/selected.txt'.format(project['path']), selected)


def error_index(error):
    key = "[NullAway] (INDEX= "
    begin = error.index(key) + len(key)
    end = error[begin:].index(")") + begin
    return int(error[begin:end])


def fix_index(fix):
    values = fix.split("$*$")
    return int(values[len(values) - 1])


def apply_fixes(fixes):
    write_lines(FIX_PATH, [str(f) for f in fixes])
    os.system("java -jar injector.jar {}".format(FIX_PATH))


def get_corresponding_fixes(error, fixes):
    return [f for f in fixes if fix_index(f) == error_index(error)]


def run():
    if not os.path.exists("/tmp/NullAwayFix/"):
        os.makedirs("/tmp/NullAwayFix/")
    with open('../../projects.json') as f:
        projects = json.load(f)
        for project in projects['projects']:
            if project['active']:
                command = "cd {} && {}".format(
                    PROJECT_DIR.format(project['path']), {})

                if not os.path.exists("./projects/{}".format(project['path'])):
                    os.makedirs("./projects/{}".format(project['path']))

                # reset
                checkout_to_branch(command, project, "base")

                # running autofixer
                run_autofix(project)
                # push everything to final branch
                checkout_to_branch(command, project, "final", save_state=True)

                # get all fixes
                os.system(
                    "mv /tmp/NullAwayFix/injected.json ./projects/{}/injected.json"
                    .format(project['path']))
                convert_json_to_csv(project['path'])
                all_fixes = read_lines('projects/{}/injected.csv'.format(
                    project['path']))
                # remove new lines from fixes
                all_fixes = [
                    f[:-1] if f[len(f) - 1] == '\n' else f for f in all_fixes
                ]

                # reset
                checkout_to_branch(command, project, "base")

                # copy the correct nullaway config
                copy_correct_nullaway_config(project)

                # select new sample errors
                select_sample_errors(command, project)

                # read sample errors
                selected = read_errors('projects/{}/selected.txt'.format(
                    project['path']))

                for i, error in enumerate(selected):
                    # reset
                    checkout_to_branch(command, project, "base")

                    _, fixes = get_error_fix(
                        PROJECT_DIR.format(project['path']),
                        command.format(project['build']))

                    # inject the initial fix
                    init_fix = get_corresponding_fixes(error, fixes)
                    apply_fixes(init_fix)

                    while True:
                        error, new_fix_base = get_error_fix(
                            PROJECT_DIR.format(project['path']),
                            command.format(project['build']))

                        new_fix_base = exclude_fixes(new_fix_base, fixes)

                        to_apply = [f for f in new_fix_base if f in all_fixes]

                        if len(to_apply) == 0:
                            print("Finished.")
                            break
                        print("Going for another round...")
                        apply_fixes(to_apply)

                    checkout_to_branch(command,
                                       project,
                                       "chain_{}".format(i),
                                       save_state=True)


run()