#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from datetime import datetime

import pytz
from generator import Generator
from stravalib.client import Client


def adjust_time(time, tz_name):
    tc_offset = datetime.now(pytz.timezone(tz_name)).utcoffset()
    return time + tc_offset


def adjust_time_to_utc(time, tz_name):
    tc_offset = datetime.now(pytz.timezone(tz_name)).utcoffset()
    return time - tc_offset


def make_activities_file(sql_file, gpx_dir, json_file):
    generator = Generator(sql_file)
    generator.sync_from_gpx(gpx_dir)
    activities_list = generator.load()
    with open(json_file, "w") as f:
        json.dump(activities_list, f, indent=0)


def make_activities_file_only(sql_file, gpx_dir, json_file):
    generator = Generator(sql_file)
    generator.sync_from_gpx(gpx_dir)
    activities_list = generator.loadForMapping()
    with open(json_file, "w") as f:
        json.dump(activities_list, f, indent=0)


def make_strava_client(client_id, client_secret, refresh_token):
    client = Client()

    refresh_response = client.refresh_access_token(
        client_id=client_id, client_secret=client_secret, refresh_token=refresh_token
    )
    client.access_token = refresh_response["access_token"]
    return client

def filter_gpx_outlier(gpx_file):
    with open(gpx_file, "r") as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    for track in gpx.tracks:
        for segment in track.segments:
            new_points = []
            last_point = None
            for point in segment.points:
                if last_point and (
                    point.distance_2d(last_point) > 1000
                    or point.distance_2d(last_point) == 0
                ):
                    # 跳过此点，因为距离上一个点太远
                    continue
                new_points.append(point)
                last_point = point
            segment.points = new_points

    with open('gpx_out/new.gpx', 'w') as output_file:
        output_file.write(gpx.to_xml())
