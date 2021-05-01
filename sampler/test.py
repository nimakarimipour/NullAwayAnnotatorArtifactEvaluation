import json

f = open('./selected_errors.json')
errors_1 = json.load(f)
f.close()


f = open('./linked.json')
errors_2 = json.load(f)
f.close()

combined = {"PROJECTS": []}

for project in errors_1['PROJECTS']:
    combined_project = project.copy()
    size_before = combined_project['size']
    size_added = 0
    for project_other in errors_2['PROJECTS']:
        if(project_other['name'] == project['name']):
            size_added = project_other['size']
            other_errors = project_other['errors'].copy()
            other_errors.extend(combined_project['errors'])
            del(combined_project['errors'])
            combined_project['errors'] = other_errors
    combined_project['size'] = len(combined_project['errors'])
    print(combined_project['size'], size_before, size_added, project['name'])
    assert combined_project['size'] == size_before + size_added
    combined['PROJECTS'].append(combined_project)

for project in combined['PROJECTS']:
    indexed_errors = []
    for i, error in enumerate(project['errors']):
        index_error = error.copy()
        index_error['index'] = i
        indexed_errors.append(index_error)
    del(project['errors'])
    project['erorrs'] = indexed_errors


with open("combined.json", "w") as f:
    json.dump(combined, f)