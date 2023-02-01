import json


def mili2min(milies):
    return milies / (1000 * 60)


def div(a, b):
    result = 100 * int(a) / int(b)
    return round(result, 2)


def table2():
    branches = ["nimak/no-opt", "nimak/pc", "nimak/p"]
    # & \hspace{1em} \texttt{Conductor} & 22.2 & 8.5 (2.6X) & 0 & 187 & 71 & 0\\\cline{1-8}
    template = "& {} & {} & {} & {} "
    with open('data/build_error_time_count.json') as f:
        projects = json.load(f)
        for project in projects:
            info = projects[project]
            total_time = info['nimak/no-opt']['time']
            total_build = info['nimak/no-opt']['build']
            line = template.format(str(div(total_time, 60 * 1000)),
                                   str(div(info['nimak/p']['time'], 60 * 1000)) + " ({}X)".format(div(total_time, info['nimak/p']['time'])),
                                   total_build,
                                   str(info['nimak/p']['build']) + " ({}X)".format(div(total_build, info['nimak/p']['build'])))
            print(project + " ----- " + line)
    # json.dump(DATA, open('nullunmarked.json', 'w'))


def table1():
    # 159 & 170 (+18.1\%) & 44 (-43.5\%) & 30 (-67.0\%)
    template = "{} & {} ({}{}\\%) & {} ({}\\%) & {} ({}\\%)"
    with open('data/build_error_time_count.json') as f:
        projects = json.load(f)
        for project in projects:
            info = projects[project]
            initial = info['initial']
            dep0 = info['nimak/exs']["error"]
            dep1 = info['nimak/p-1']["error"]
            dep5 = info['nimak/p']["error"]
            line = template.format(initial,
                                   dep0,
                                   "+" if dep0 > initial else "", div(dep0 - initial, initial),
                                   dep1, div(dep1 - initial, initial),
                                   dep5, div(dep5 - initial, initial))
            print(project + " " + line)
    # json.dump(DATA, open('nullunmarked.json', 'w'))


def table3():
    template = "{} & {} & {}"
    unchecked = json.load(open('data/unchecked.json', 'r'))
    with open('data/annotation_count.json') as f:
        projects = json.load(f)
        for project in projects:
            info = projects[project]
            nullable = info['nimak/p']['nullable']
            null_unmarked = info['nimak/p']['nullunmarked']
            suppress = info['nimak/p']['suppress']
            suppress_init = info['nimak/p']['suppress_init']
            unchecked_p = unchecked[project]["nimak/p-nullunmarked"]
            total_line = unchecked[project]["initial"]
            line = template.format(nullable, null_unmarked + suppress_init + suppress, div(unchecked_p, total_line))
            print(project + " ------- " + line)


def unchecked_inference_off():
    unchecked = json.load(open('data/unchecked.json', 'r'))
    template = "{} on: {} off: {} div: {}"
    for project in unchecked:
        info = unchecked[project]
        on = div(info['nimak/p-nullunmarked'], info['initial'])
        off = div(info['nullaway-nullunmarked'], info['initial'])
        print(template.format(project, on, off, round(off / on, 2)))


def speed_up_depth1():
    projects = json.load(open('data/build_error_time_count.json', 'r'))
    avg = 0
    for project in projects:
        print(project)
        info = projects[project]
        avg += info['nimak/p']['time'] / info['nimak/p-1']['time']
    print(avg / len(projects))


unchecked_inference_off()
