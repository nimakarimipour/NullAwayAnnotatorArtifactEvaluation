import json

MAC = "/Users/nima/Developer/NullAwayFixer/Projects/"
LINUX = "/home/nima/Developer/AutoFixer/Evaluation/Projects/"
DISP = "{}|{}|{}|{}"
HYPER_LINK = "\"=HYPERLINK(\"\"{}\"\",\"\"{}\"\")\""

def make_csv():
    LINES = ["\"Project\"|\"Error\"|\"Chain\"|\"TYPE\"\n"]
    with open('../../projects.json') as f:
        projects = json.load(f)
        for project in projects['projects']:
            if(project['active'] == False):
                continue
            with open("../chain/projects/{}/selected.txt".format(project['path'])) as f:
                errors = [l for i, l in enumerate(f.readlines()) if i % 5 == 0]
                for i, error in enumerate(errors):
                    start = len(MAC) if error.startswith(MAC) else len(LINUX)
                    error_link = error[start:error.find(": error: [NullAway]")].replace(":", "#L")
                    start = error_link.find(project['path']) + len(project['path'])
                    error_link = "{}/blob/base{}".format(error_link[:start], error_link[start:])
                    error_link = "https://github.com/nimakarimipour/{}".format(error_link)
                    name = project['name']
                    error_disp = HYPER_LINK.format(error_link, "error_{}".format(i))
                    branch = HYPER_LINK.format("https://github.com/nimakarimipour/{}/tree/chain_{}".format(project['path'], i), "chain_{}".format(i))
                    type = error[error.find(" (Covered) ") + len(" (Covered) "):]
                    if("method does not guarantee @NonNull fields" in type ):
                        type = "method does not guarantee intialization of @NonNull fields\n"
                    disp = DISP.format(name, error_disp, branch, type)
                    LINES.append(disp)


    with open('data.csv', "w") as f:
        f.writelines(LINES)

make_csv()
