#!/bin/python

import argparse
import os
import json
import shutil
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), ".."))

from Benchmark import *

##
# Mad Max benchmark.
##
class MadMax(Benchmark):
    def __init__(self, resolution, iterations):
        Benchmark.__init__(self, "MadMax")
        self._game_path = os.environ['HOME'] + "/work/Steam/steamapps/common/Mad Max"
        self._conf_path = os.environ['HOME'] + "/.local/share/feral-interactive/Mad Max/"
        self._log_path = os.environ['HOME'] + "/.local/share/feral-interactive/Mad Max/VFS/User/AppData/Roaming/WB Games/Mad Max/FeralBenchmark"
        self._resolution = resolution
        self._iterations = iterations
        self._preset = "ultra"
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
        self.run_process(["./MadMax", "-feral-benchmark"])
        os.chdir(olddir)

    def bench(self):
        for i in range(0, self._iterations):
            self.run()
            self._fps.append(self.get_fps())

    def get_fps_for_scene(self, name):
        log_dir = self.get_latest_file(self._log_path)
        log_file = log_dir + "/benchmark_" + str(name) + ".xml"
        fps = []
        with open(log_file, "r") as f:
            for line in f:
                if "avg_fps" in line:
                    value = re.search('<value name="avg_fps">(.*)</value>', line).group(1)
                    return round_fps(value)
        return 0

    def get_fps(self):
        fps = {}
        fps["camp-hollow"] = self.get_fps_for_scene("1")
        fps["stronghold"] = self.get_fps_for_scene("2")
        fps["hope-glory"] = self.get_fps_for_scene("3")
        fps["landmover"] = self.get_fps_for_scene("4")
        return fps

    def print_result(self, scene):
        # Compute avg, min and max for this scene.
        fps = []
        for data in self._fps:
            fps.append(data[scene])
        min_fps = min(fps)
        max_fps = max(fps)
        avg_fps = sum(fps) / self._iterations

        # Print result for this scene.
        result = {}
        result['app'] = str(self.name)
        result['resolution'] = str(self._resolution)
        result['preset'] = str(self._preset)
        result['scene'] = str(scene)
        result['avg_fps'] = str(avg_fps)
        result['min_fps'] = str(min_fps)
        result['max_fps'] = str(max_fps)
        result['interations'] = str(self._iterations)
        print(result)

    def print_results(self):
        self.print_result("camp-hollow")
        self.print_result("stronghold")
        self.print_result("hope-glory")
        self.print_result("landmover")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mad Max benchmark")
    parser.add_argument('--iterations', type=int, default=3)
    parser.add_argument('--dry-run', type=bool, default=True)
    parser.add_argument('--resolution', type=str, default='1920x1080',
                        choices=['1920x1080', '2560x1440', '3840x2160'])
    args = parser.parse_args(sys.argv[1:])

    madmax = MadMax(args.resolution, args.iterations)
    madmax.install()
    if args.dry_run:
        madmax.run() # For compiling pipelines
    madmax.bench()
    madmax.print_results()
