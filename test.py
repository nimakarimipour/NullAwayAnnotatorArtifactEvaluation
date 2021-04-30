import json

end = 2
start = 1
project = {"name": "test"}

time_json_file = open('time.json')
times = json.load(time_json_file)
time_json_file.close()
times[project['name']] = {"total": end - start}
time_json_file = open('time.json', "w")
json.dump(times, time_json_file)
time_json_file.close()