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
    with open('../data/mp_zuul.json') as f:
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


def table1fromUber():
    # \hspace{1em} \texttt{Zuul} & 15.2K & 204 & 174 (-14.7\%) & 82 (-59.8\%) & 71 (-65.2\%)\\\cline{1-7}
    template = "& \\hspace{{1em}} \\texttt{{{}}} & {} & {} & {} & {} & {} \\\\\\cline{{2-7}}"
    data = ['T1', '35.7K', '537', '457', '203', '190', 'T2', '81.7K', '1072', '991', '322', '311', 'T3', '12.9K', '229', '134', '45', '31', 'T4', '20.1K', '111', '70', '70', '70', 'T5', '13.8K', '222', '195', '129', '129', 'T6', '3.4K', '47', '61', '10', '9', 'T7', '5.9K', '35', '28', '21', '19', 'T8', '14.8K', '301', '167', '92', '76']
    #        0       1       2     3      4      5
    for i in range(0, 8):
        current = 6 * i
        initial = int(data[current + 2])
        depth0 = int(data[current + 3])
        depth1 = int(data[current + 4])
        depth5 = int(data[current + 5])
        line = template.format("T{}".format(i),
                               data[current + 1],
                               initial,
                               "{} ({}\\%)".format(depth0, round((1 - depth0 / initial) * 100, 1)),
                               "{} ({}\\%)".format(depth1, round((1 - depth1 / initial) * 100, 1)),
                               "{} ({}\\%)".format(depth5, round((1 - depth5 / initial) * 100, 1))
                               )
        print(line)

table1fromUber()