#!/bin/python

import argparse
import os
import json
import shutil
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), ".."))

from enum import Enum
from Benchmark import *

##
# The Talos Principale benchmark.
##
class Talos_api(Enum):
    OPENGL = "OpenGL"
    VULKAN = "VLK"
    def __str__(self):
        return self.value

class Talos(Benchmark):
    def __init__(self, api, resolution, iterations):
        Benchmark.__init__(self, "Talos")
        self._game_path = os.environ['HOME'] + "/.steam/steam/steamapps/common/The Talos Principle"
        self._demo_file = os.path.dirname(os.path.realpath(__file__)) + "/bench.lua"
        self._conf_path = os.environ['HOME'] + "/.steam/steam/userdata/327368460/257510/local/"
        self._api = api
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
        return dirname + "/Talos.ini"

    def install(self):
        conf_file = self.get_config_file()
        shutil.copyfile(conf_file, self._conf_path + "Talos.ini")

    def run(self):
        olddir = os.getcwd()
        os.chdir(self._game_path + "/Bin/x64")
        os.environ['SteamAppId'] = str(257510)
        n = self._resolution.find('x')
        width = self._resolution[:n]
        height = self._resolution[n+1:]
        cmd = ['./Talos',
               '+exec', self._demo_file,
               '+gfx_strAPI', str(self._api),
               '+gfx_pixResWidth', str(width),
               '+gfx_pixResHeight', str(height)]
        self.run_process(cmd)
        os.chdir(olddir)

    def bench(self):
        for i in range(0, self._iterations):
            self.run()
            self._fps.append(self.get_fps())

    def get_fps(self):
        log_file = self._game_path + "/Log/Talos.log"
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
    parser = argparse.ArgumentParser(description="The Talos Principale benchmark")
    parser.add_argument('--iterations', type=int, default=3)
    parser.add_argument('--dry-run', type=int, default=1)
    parser.add_argument('--api', type=Talos_api,
                        default=Talos_api.VULKAN,
                        choices=list(Talos_api))
    parser.add_argument('--resolution', type=str, default='1920x1080',
                        choices=['1920x1080', '2560x1440', '3840x2160'])
    args = parser.parse_args(sys.argv[1:])

    talos = Talos(args.api, args.resolution, args.iterations)
    talos.install()
    talos.cleanup()
    if args.dry_run:
        talos.run() # For compiling pipelines
    talos.bench()
    talos.print_results()
