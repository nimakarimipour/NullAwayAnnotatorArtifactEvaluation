import json


def div(a, b):
    result = int(a) / int(b)
    return round(result, 1)


def table2():
    branches = ["nimak/no-opt", "nimak/pc", "nimak/p"]
    # & \hspace{1em} \texttt{Conductor} & 22.2 & 8.5 (2.6X) & 0 & 187 & 71 & 0\\\cline{1-8}
    template = "& \\hspace{{1em}} \\texttt{{{}}} & {} & {} & {} & {} & {} & {} \\\\\\cline{{2-8}}"
    with open('../data/result.json') as f:
        projects = json.load(f)
        for project in projects:
            info = projects[project]
            total_time = int(info['nimak/no-opt']['time'])
            total_build = int(info['nimak/no-opt']['build'])
            line = template.format(project,
                                   div(total_time, (60 * 1000)),
                                   str(div((info['nimak/p']['time']), 60 * 1000)),
                                   str(div(int(info['nimak/pc']['time']), 60 * 1000)),
                                   total_build,
                                   str(info['nimak/p']['build']),
                                   str(info['nimak/pc']['build']))
            print(line)
    # json.dump(DATA, open('nullunmarked.json', 'w'))


def table1():
    branches = ["nimak/no-opt", "nimak/p"]
    # & \hspace{1em} \texttt{Conductor} & 22.2 & 8.5 (2.6X) & 0 & 187 & 71 & 0\\\cline{1-8}
    template = "& \\hspace{{1em}} \\texttt{{{}}} & {} & {} & {} & {} & {} & {} \\\\\\cline{{2-8}}"
    with open('../data/result.json') as f:
        projects = json.load(f)
        for project in projects:
            info = projects[project]
            total_time = int(info['nimak/no-opt']['time'])
            total_build = int(info['nimak/no-opt']['build'])
            line = template.format(project,
                                   div(total_time, (60 * 1000)),
                                   str(div((info['nimak/p']['time']), 60 * 1000)),
                                   str(div(int(info['nimak/pc']['time']), 60 * 1000)),
                                   total_build,
                                   str(info['nimak/p']['build']),
                                   str(info['nimak/pc']['build']))
            print(line)
    # json.dump(DATA, open('nullunmarked.json', 'w'))


def table3():
    # depth0 @Nullable @Suppress @Remaining @Percentage
    # & \texttt{Conductor}& 157 & 114 & 0 & 0 & 0 \\\cline{2-8}
    template = "& \\texttt{{{}}} & {} & {} & {} & {} & \%{} \\\\\\cline{{2-7}}"
    with open('../data/annotation.json') as f:
        projects = json.load(f)
        null_unmarked_data = json.load(open('../data/nullunmarked.json', 'r'))
        for project in projects:
            info = projects[project]
            null_info = null_unmarked_data[project]
            null_0 = info['depth0']
            null_5 = info['nullable']
            suppress = info['suppress'] + info['suppress_init'] + info['nullunmarked']
            remaining = null_info['nimak/nullunmarked']['errors']
            percent = round(null_info['unchecked'] / null_info['total'] * 100, 2)
            line = template.format(project, null_0, null_5, suppress, remaining, percent)
            print(line)


table1()