#! /usr/bin/env nix-shell
#! nix-shell -i python3 -p python3Packages.pyyaml python3Packages.pytz
import subprocess
import yaml
import sys
from datetime import datetime
import pytz

def get_leaders_dates():
    jcli = subprocess.check_output(["jcli", "rest", "v0", "leaders", "logs", "get", "-h", "http://127.0.0.1:8443/api"]);
    decoded = jcli.decode(sys.stdout.encoding);
    load_yaml = yaml.safe_load(decoded);
    dates = [];
    for event in range(len(load_yaml)):
      dates.append((load_yaml[event]['scheduled_at_time']));
    dates.sort(key = lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S+00:00'));
    return dates;

def main():
    dates = get_leaders_dates();
    now = datetime.now().astimezone(pytz.utc)
    dates_list = [datetime.strptime(date, '%Y-%m-%dT%H:%M:%S+00:00').replace(tzinfo=pytz.utc)for date in dates]
    youngest = min(dt for dt in dates_list if dt > now)
    seconds_until_next_event = int((youngest - now).total_seconds())
    print("You next leader event is at {0} in {1} seconds.".format(youngest, seconds_until_next_event));

if __name__== "__main__":
    main()
