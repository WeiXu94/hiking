import json

from generator import Generator


def make_activities_file(sql_file, gpx_dir, json_file):
    generator = Generator(sql_file)
    generator.sync_from_gpx(gpx_dir)
    activities_list = generator.load()
    with open(json_file, "w") as f:
        json.dump(activities_list, f, indent=2)

def make_activities_file_only(sql_file, json_file):
    generator = Generator(sql_file)
    activities_list = generator.loadForMapping()
    with open(json_file, "w") as f:
        json.dump(activities_list, f, indent=2)
