import os
import json
import sys

# Run with Python2
PROJECT_DIR = "/tmp/projects/{}"
DISP = "{} & {} & {} & {}\n"
BRANCH = 'nimak/pc'
CONFIG = json.load(open("annotator-config.json", 'r'))
PARALLEL_PROCESSING = True
CACHE = True
GIT_KEY = "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"
GIT = "https://nimakarimipour:{}@github.com/nimakarimipour/{}.git".format(GIT_KEY, {})

CONFIGURATIONS = [
    {
        "PARALLEL_PROCESSING": True,
        "CACHE": True,
        "BRANCH": "nimak/pc"
    },
    {
        "PARALLEL_PROCESSING": True,
        "CACHE": False,
        "BRANCH": "nimak/p"
    },
]


def execute(command):
    print("Executing: " + command, flush=True)
    sys.stdout.flush()
    os.system(command)


with open('projects.json') as f:
    execute("cd /tmp/ && mkdir projects")
    projects = json.load(f)
    for project in projects['projects']:
        if project['path'] != 'litiengine':
            continue
        if project['active']:
            execute("cd /tmp/projects && git --single-branch --branch nullaway clone {}".format(GIT.format(project['path'])))
            project_dir = PROJECT_DIR.format(project['path'])
            COMMAND = "cd {} && {}".format(project_dir, {})
            for configuration in CONFIGURATIONS:
                parallel_processing = configuration['PARALLEL_PROCESSING']
                cache = configuration['CACHE']
                branch = configuration['BRANCH']
                execute("rm -rvf /tmp/NullAwayFix")
                execute(COMMAND.format("git reset --hard"))
                execute(COMMAND.format("git checkout nullaway"))
                execute(COMMAND.format("git reset --hard"))
                execute(COMMAND.format("git branch -D {}".format(branch)))
                execute(COMMAND.format("git checkout -b {}".format(branch)))
                local_config = json.load(open(project_dir + "/annotator-config.json", "r"))
                config = CONFIG.copy()
                config['BUILD_COMMAND'] = "cd {} && {}".format(project_dir,
                                                               local_config['BUILD_COMMAND'].split(' && ')[1])
                config['ANNOTATION']['INITIALIZER'] = local_config['ANNOTATION']['INITIALIZER']
                config['ANNOTATION']['NULLABLE'] = local_config['ANNOTATION']['NULLABLE']
                config['ANNOTATION']['NULL_UNMARKED'] = local_config['ANNOTATION']['NULL_UNMARKED']
                config['PARALLEL_PROCESSING'] = parallel_processing
                config['CACHE_IMPACT_ACTIVATION'] = cache
                with open('/tmp/NullAwayAnnotator/runner/config.json', 'w') as outfile:
                    json.dump(config, outfile)
                execute(
                    "cd /tmp/NullAwayAnnotator/runner && ./start.sh --path /tmp/NullAwayAnnotator/runner/config.json")
                execute("mv /tmp/NullAwayFix {}/AnnotatorOut".format(project_dir))
                execute(COMMAND.format("git add ."))
                execute(COMMAND.format(
                    'git commit -m "Annotator result Parallel:{} Cache:{}"'.format(parallel_processing, cache)))
                execute(COMMAND.format("git push {} --delete {}".format(GIT.format(project['path']), branch)))
                execute(COMMAND.format("git push --set-upstream {} {}".format(GIT.format(project['path']), branch)))
