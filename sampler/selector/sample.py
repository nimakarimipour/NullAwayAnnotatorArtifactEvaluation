import json
import random

selected_errors = []

# Only run with python3

with open('./errors.json') as f:

    projects = json.load(f)['PROJECTS']
    total_num = 0
    for project in projects.values():
        total_num += project['size']

    for name, project in projects.items():
        toSelectSize = int(150 * (project['size'] / total_num))
        if (toSelectSize < 5):
            toSelectSize = 5
        if (project['size'] < toSelectSize):
            toSelectSize = project['size']
        indecies = random.sample(range(0, project['size']), toSelectSize)
        errors_in_project = project['errors']
        selected_errors_in_project = []
        for index in indecies:
            selected_errors_in_project.append(errors_in_project[index])
        final_select = {}
        final_select['name'] = name
        final_select['size'] = toSelectSize
        final_select['errors'] = selected_errors_in_project
        selected_errors.append(final_select)

outfilename = "selected_errors.json"
result = {}
result['PROJECTS'] = selected_errors
with open(outfilename, 'w') as outfile:
    json.dump(result, outfile)