import os
import json
import sys

# Run with Python2
PROJECT_DIR = "/tmp/projects/{}"
DISP = "{} & {} & {} & {}\n"
CONFIG = json.load(open("annotator-config.json", 'r'))
project_name = sys.argv[1]
optimized = False if (len(sys.argv) == 3 and sys.argv[2] == '--disable-optimization') else True
java = {
    8: "export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/ && update-alternatives --set java /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java && update-alternatives --set javac /usr/lib/jvm/java-8-openjdk-amd64/bin/javac",
    11: "export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64/ && update-alternatives --set java /usr/lib/jvm/java-11-openjdk-amd64/bin/java && update-alternatives --set javac /usr/lib/jvm/java-11-openjdk-amd64/bin/javac",
    17: "export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64/ && update-alternatives --set java /usr/lib/jvm/java-17-openjdk-amd64/bin/java && update-alternatives --set javac /usr/lib/jvm/java-17-openjdk-amd64/bin/javac"
}


def execute(command):
    print("Executing: " + command, flush=True)
    sys.stdout.flush()
    os.system(command)


def pepare_java(project):
    execute(java[project['java']])


with open('projects.json') as f:
    projects = json.load(f)
    for project in projects['projects']:
        if project['name'] == project_name:
            pepare_java(project)
            project_dir = PROJECT_DIR.format(project['path'])
            COMMAND = "cd {} && {}".format(project_dir, {})
            execute("rm -rvf /tmp/NullAwayFix")
            local_config = json.load(open(project_dir + "/annotator-config.json", "r"))
            config = CONFIG.copy()
            config['BUILD_COMMAND'] = "cd {} && {}".format(project_dir,
                                                           local_config['BUILD_COMMAND'].split(' && ')[1])
            config['ANNOTATION']['INITIALIZER'] = local_config['ANNOTATION']['INITIALIZER']
            config['ANNOTATION']['NULLABLE'] = local_config['ANNOTATION']['NULLABLE']
            config['ANNOTATION']['NULL_UNMARKED'] = local_config['ANNOTATION']['NULL_UNMARKED']
            config['PARALLEL_PROCESSING'] = optimized
            with open('/tmp/NullAwayAnnotator/runner/config.json', 'w') as outfile:
                json.dump(config, outfile)
            execute(
                "cd /tmp/NullAwayAnnotator/runner && ./start.sh --path /tmp/NullAwayAnnotator/runner/config.json")
