import json

def link_for_errors():
    with open('../../projects.json') as f:
        projects = json.load(f)
        for project in projects['projects']:
            if(project['active'] == False):
                continue
            with open("../chain/projects/{}/selected.txt".format(project['path'])) as f:
                errors = [l for i, l in enumerate(f.readlines()) if i % 4 == 0]
                for error in errors:
                    print(error[error.find("/Users/nima/Developer/NullAwayFixer/Projects/"):error.find(": error: [NullAway]")])
                exit()

link_for_errors()


# https://github.com/nimakarimipour/MPAndroidChart/blob/base/MPChartLib/src/main/java/com/github/mikephil/charting/charts/Chart.java#L699