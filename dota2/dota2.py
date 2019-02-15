#!/bin/python

import argparse
import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), ".."))

from Benchmark import *

##
# Dota2 benchmark.
##
class Dota2(Benchmark):
    def __init__(self, iterations):
        Benchmark.__init__(self, "Dota2")
        self._game_path = os.environ['HOME'] + "/work/Steam/steamapps/common/dota 2 beta"
        self._iterations = iterations
        self._fps = []

    def run(self):
        olddir = os.getcwd()
        os.chdir(self._game_path + "/game")
        self.run_process(["./dota.sh", "+con_logfile \$LOG_FILE +timedemoquit dota2-pts-1971360796 +demo_quitafterplayback 1 +cl_showfps 2 +fps_max 0 -nosound -noassert -console -fullscreen +timedemo_start 50000 +timedemo_end 51000 -autoconfig_level 3 -testscript_inline \\\"Test_WaitForCheckPoint DemoPlaybackFinished\; quit\\\" -vulkan"])
        os.chdir(olddir)

    def bench(self):
        for i in range(0, self._iterations):
            self.run()
            self._fps.append(self.get_fps())

    def get_fps(self):
        log_file = self._game_path + "/game/dota/Source2Bench.csv"
        with open(log_file) as f:
            data = f.readlines()
        lastline = data[-1]
        data = lastline.split(',')
        return float(data[2])

    def get_min_fps(self):
        return min(self._fps)

    def get_max_fps(self):
        return max(self._fps)

    def get_avg_fps(self):
        return sum(self._fps) / self._iterations

    def get_results(self):
        results = {}
        results['app'] = str(self.name)
        results['avg_fps'] = str(self.get_avg_fps())
        results['min_fps'] = str(self.get_min_fps())
        results['max_fps'] = str(self.get_max_fps())
        results['iterations'] = str(self._iterations)
        return results

    def print_results(self):
        print(json.dumps(self.get_results()))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dota2 benchmark")
    parser.add_argument('--iterations', type=int, default=3)
    parser.add_argument('--dry-run', type=int, default=1)
    args = parser.parse_args(sys.argv[1:])

    dota2 = Dota2(args.iterations)
    if args.dry_run:
        dota2.run() # For compiling pipelines
    dota2.bench()
    dota2.print_results()
