#!/bin/python

import os
import re
import sys
import getopt
import subprocess
import time
import tempfile
import glob
import argparse

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), ".."))

from enum import Enum
from Benchmark import *
from Util import *

def getpid(name):
    return int(check_output(["pidof", "-s", name]))

##
# Rise of The Tomb Raider benchmark.
##
class ROTR_preset(Enum):
    LOWEST = "Lowest"
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    VERY_HIGH = "VeryHigh"
    def __str__(self):
        return self.value

class ROTR_antialiasing(Enum):
    OFF = "off"
    FXAA = "fxaa"
    SMAA = "smaa"
    SSAA_2X = "ssaa_2x"
    SSAA_4X = "ssaa_4x"
    def __str__(self):
        return self.value

class ROTR(Benchmark):
    def __init__(self, resolution, preset, antialiasing, iterations):
        self._game_path = os.environ['HOME'] + "/work/Steam/steamapps/common/Rise of the Tomb Raider/"
        self._conf_path = os.environ['HOME'] + "/.local/share/feral-interactive/Rise of the Tomb Raider/"
        self._resolution = resolution
        self._preset = preset.value
        self._antialiasing = antialiasing
        self._iterations = iterations
        self._fps = []

    def get_config_file(self):
        dirname = os.path.dirname(os.path.realpath(__file__))
        return dirname + "/preferences.xml"

    def convert_antialiasing(self):
        if self._antialiasing == ROTR_antialiasing.OFF:
            return 0
        elif self._antialiasing == ROTR_antialiasing.FXAA:
            return 1
        elif self._antialiasing == ROTR_antialiasing.SMAA:
            return 2
        elif self._antialiasing == ROTR_antialiasing.SSAA_2X:
            return 3
        elif self._antialiasing == ROTR_antialiasing.SSAA_4X:
            return 4

    def install(self):
        conf = get_file_contents(self.get_config_file())
        n = self._resolution.find('x')
        conf = conf.replace('@ScreenW@', self._resolution[:n])
        conf = conf.replace('@ScreenH@', self._resolution[n+1:])
        conf = conf.replace('@DefaultPreset@', self._preset)
        conf = conf.replace('@DefaultAntialiasing@', str(self.convert_antialiasing()))
        olddir = os.getcwd()
        os.chdir(self._conf_path)
        with open(self._conf_path + "preferences", 'w+') as f:
            f.write(conf)
        os.chdir(olddir)

    def run(self):
        olddir = os.getcwd()
        os.chdir(self._game_path)
        cmd = ["./RiseOfTheTombRaider.sh"]
        proc = self.run_process(cmd)
        # Wait to be sure the application is started.
        self.run_process(["sleep", "5"])
        # Get PID.
        pid = getpid("RiseOfTheTombRaider")
        # Wait until the process is done.
        while os.path.exists("/proc/%s" % str(pid)):
            time.sleep(1)
        os.chdir(olddir)

    def bench(self):
        for i in range(0, self._iterations):
            self.run()
            self._fps.append(self._get_fps())

    def _get_fps_for_scene(self, name):
        log_path = self._conf_path + "VFS/User/AppData/Roaming/Rise of the Tomb Raider/"
        all_files = glob.glob(log_path + "/" + name + "_*")
        list_of_files = []
        # Exclude some files.
        for f in all_files:
            if not "frametimes" in f:
                list_of_files.append(f)
        # Get the latest file and extract the average number of FPS.
        latest_file = max(list_of_files, key=os.path.getctime)
        with open(latest_file, 'r') as f:
            for line in f.readlines():
                if "Average FPS:" in line:
                    return re.search("Average FPS: (.*)", line).group(1)
        return 0

    def _get_fps(self):
        fps = {}
        fps["SpineOfTheMountain"] = self._get_fps_for_scene("SpineOfTheMountain")
        fps["ProphetsTomb"] = self._get_fps_for_scene("ProphetsTomb")
        fps["GeothermalValley"] = self._get_fps_for_scene("GeothermalValley")
        return fps

    def print_results(self):
        results = {}
        results['app'] = str(self.name)
        results['resolution'] = str(self._resolution)
        results['preset'] = str(self._preset)
        results['antialiasing'] = str(self._antialiasing)
        results['interations'] = str(self._iterations)
        print(results)
        print(self._fps)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rise Of The Tomb Raider benchmark")
    parser.add_argument('--iterations', type=int, default=1)
    parser.add_argument('--resolution', type=str, default='1920x1080',
                        choices=['1920x1080', '2560x1440', '3840x2160'])
    parser.add_argument('--preset', type=ROTR_preset,
                        default=ROTR_preset.VERY_HIGH,
                        choices=list(ROTR_preset))
    parser.add_argument('--antialiasing', type=ROTR_antialiasing,
                        default=ROTR_antialiasing.FXAA,
                        choices=list(ROTR_antialiasing))
    args = parser.parse_args(sys.argv[1:])

    rotr = ROTR(args.resolution, args.preset, args.antialiasing, args.iterations)
    rotr.install()
    rotr.bench()
    rotr.print_results()
