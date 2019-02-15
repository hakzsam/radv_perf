#!/bin/python

import argparse
import os
import json
import shutil
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), ".."))

from Benchmark import *

def getpid(name):
    return int(check_output(["pidof", "-s", name]))

##
# Serious Sam 2017 benchmark.
##

class Sam2017(Benchmark):
    def __init__(self, resolution, iterations):
        Benchmark.__init__(self, "Sam2017")
        self._game_path = os.environ['HOME'] + "/work/Steam/steamapps/common/Serious Sam Fusion 2017"
        self._demo_file = os.environ['HOME'] + "/pts-tfe-fusion-run.lua"
        self._conf_path = os.environ['HOME'] + "/work/Steam/userdata/327368460/564310/local/"
        self._resolution = resolution
        self._iterations = iterations
        self._fps = []

    def cleanup(self):
        # Cleanup in case the game didn't exit properly last time.
        lock = self._game_path + "/Temp/run.txt"
        if os.path.isfile(lock):
            os.remove(lock)

    def get_config_file(self):
        dirname = os.path.dirname(os.path.realpath(__file__))
        return dirname + "/SeriousSam2017.ini"

    def install(self):
        conf_file = self.get_config_file()
        shutil.copyfile(conf_file, self._conf_path + "SeriousSam2017.ini")

    def run(self):
        olddir = os.getcwd()
        os.chdir(self._game_path)
        n = self._resolution.find('x')
        width = self._resolution[:n]
        height = self._resolution[n+1:]
        cmd = ["steam",
               "-applaunch", "564310",
               "+exec", self._demo_file,
               "+gfx_pixResWidth", str(width),
               "+gfx_pixResHeight", str(height)]
        proc = self.run_process(cmd)
        # Wait to be sure the application is started.
        self.run_process(["sleep", "5"])
        # Get PID.
        pid = getpid("Sam2017")
        # Wait until the process is done.
        while os.path.exists("/proc/%s" % str(pid)):
            time.sleep(1)
        os.chdir(olddir)

    def bench(self):
        for i in range(0, self._iterations):
            self.run()
            self._fps.append(self.get_fps())

    def get_fps(self):
        log_file = self._game_path + "/Log/Sam2017.log"
        with open(log_file, "r") as f:
            for line in f:
                if "Average" in line:
                    value = re.search('Average: (.*) FPS', line).group(1)
                    return round_fps(value)
        return 0

    def get_min_fps(self):
        return min(self._fps)

    def get_max_fps(self):
        return max(self._fps)

    def get_avg_fps(self):
        return sum(self._fps) / self._iterations

    def get_results(self):
        results = {}
        results['app'] = str(self.name)
        results['resolution'] = str(self._resolution)
        results['avg_fps'] = str(self.get_avg_fps())
        results['min_fps'] = str(self.get_min_fps())
        results['max_fps'] = str(self.get_max_fps())
        results['iterations'] = str(self._iterations)
        return results

    def print_results(self):
        print(json.dumps(self.get_results()))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Serious Sam 2017 benchmark")
    parser.add_argument('--iterations', type=int, default=3)
    parser.add_argument('--dry-run', type=int, default=1)
    parser.add_argument('--resolution', type=str, default='1920x1080',
                        choices=['1920x1080', '2560x1440', '3840x2160'])
    args = parser.parse_args(sys.argv[1:])

    sam2017 = Sam2017(args.resolution, args.iterations)
    sam2017.cleanup()
    sam2017.install()
    if args.dry_run:
        sam2017.run() # For compiling pipelines
    sam2017.bench()
    sam2017.print_results()
