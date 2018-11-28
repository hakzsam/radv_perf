#!/bin/python

import argparse
import os
import shutil
import sys

from enum import Enum

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), ".."))

from Benchmark import *

##
# Dawn Of War III benchmark.
##
class DOW3_preset(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    MAXIMUM = "max"
    ULTRA = "ultra"
    def __str__(self):
        return self.value

class DOW3(Benchmark):
    def __init__(self, preset, iterations):
        Benchmark.__init__(self, "DOW3")
        self._game_path = os.environ['HOME'] + "/work/Steam/steamapps/common/Dawn of War III"
        self._conf_path = os.environ['HOME'] + "/.local/share/feral-interactive/Dawn of War III/"
        self._log_path = os.environ['HOME'] + "/.local/share/feral-interactive/Dawn of War III/VFS/User/AppData/Roaming/My Games/Dawn of War III/LogFiles/"
        self._preset = str(preset)
        self._iterations = iterations
        self._fps = []

    def get_config_file(self):
        dirname = os.path.dirname(os.path.realpath(__file__))
        return dirname + "/preferences." + self._preset + ".xml"

    def install(self):
        pref_file = self._conf_path + "preferences"
        conf_file = self.get_config_file()
        shutil.copyfile(conf_file, pref_file)

    def run(self):
        olddir = os.getcwd()
        os.chdir(self._game_path + "/bin")
        cmd =  ["./DawnOfWar3",
                "-autotest autotest/performance_test.lua -perftest"]
        self.run_process(cmd)
        os.chdir(olddir)

    def bench(self, dry_run = False):
        for i in range(0, self._iterations):
            self.run()
            self._fps.append(self._get_fps())

    def _get_fps(self):
        log_file = self.get_latest_file(self._log_path)

        with open(log_file, "r") as f:
            for line in f:
                if "average fps" in line:
                    value = re.search("average fps,(.*)", line).group(1)
                    return round_fps(value)
        return 0

    def get_min_fps(self):
        return min(self._fps)

    def get_max_fps(self):
        return max(self._fps)

    def get_avg_fps(self):
        return sum(self._fps) / self._iterations

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dawn of War III benchmark")
    parser.add_argument('--iterations', type=int, default=3)
    parser.add_argument('--dry-run', type=bool, default=True)
    parser.add_argument('--preset', type=DOW3_preset,
                        default=DOW3_preset.ULTRA,
                        choices=list(DOW3_preset))
    args = parser.parse_args(sys.argv[1:])

    dow3 = DOW3(args.preset, args.iterations)
    dow3.install()
    if args.dry_run:
        dow3.run() # For compiling pipelines
    dow3.bench()
    min_fps = dow3.get_min_fps()
    max_fps = dow3.get_max_fps()
    avg_fps = dow3.get_avg_fps()
    print("DOW3 (avg: %s, min: %s, max: %s)" % (str(avg_fps), str(min_fps), str(max_fps)))
