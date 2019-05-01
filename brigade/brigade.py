#!/bin/python3

import argparse
import os
import json
import sys
import glob
import time

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), ".."))

from enum import Enum
from Benchmark import *
from Util import *

STEAM_DIR = os.environ['HOME'] + "/work/Steam"
#STEAM_DIR = os.environ['HOME'] + "/.steam/steam"

##
# Strange Brigade benchmark.
##
class Brigade_preset(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    ULTRA = "Ultra"
    def __str__(self):
        return self.value

class Brigade(Benchmark):
    def __init__(self, proton, resolution, preset, iterations):
        Benchmark.__init__(self, "Strange Brigade")
        self._game_path = STEAM_DIR + "/steamapps/common/StrangeBrigade"
        self._conf_path = STEAM_DIR + "/steamapps/compatdata/312670"
        self._proton = proton
        self._preset = preset.value
        self._resolution = resolution
        self._iterations = iterations
        self._fps = []

    def get_config_file(self):
        dirname = os.path.dirname(os.path.realpath(__file__))
        return dirname + "/GraphicsOptions_%s.ini" % self._preset

    def install(self):
        conf_file = get_file_contents(self.get_config_file())

        n = self._resolution.find('x')
        width = self._resolution[:n]
        height = self._resolution[n+1:]
        conf_file = conf_file.replace('RESOLUTION_WIDTH', width)
        conf_file = conf_file.replace('RESOLUTION_HEIGHT', height)

        with open(self._conf_path + "/pfx/drive_c/users/steamuser/Local Settings/Application Data/Strange Brigade/GraphicsOptions.ini", 'w+') as f:
            f.write(conf_file)

    def run(self):
        olddir = os.getcwd()
        os.chdir(self._game_path + "/bin")

        proton_dir = STEAM_DIR + '/steamapps/common/Proton %s/' % self._proton
        cmd = [proton_dir + 'proton', 'run', './StrangeBrigade_Vulkan.exe', '-skipdrivercheck', '-noHDR', '-benchmark']
        os.environ['STEAM_COMPAT_DATA_PATH'] = self._conf_path
        os.environ['SteamAppId'] = str(312670)
        self.run_process(cmd)
        time.sleep(3) # Not sure why this is needed.

        os.chdir(olddir)

    def bench(self):
        for i in range(0, self._iterations):
            self.run()
            self._fps.append(self.get_fps())

    def get_fps(self):
        log_path = self._conf_path + "/pfx/drive_c/users/steamuser/My Documents/StrangeBrigade_Benchmark"
        all_files = glob.glob(log_path + "/SB__*.txt")
        # Get the latest file and extract the average number of FPS.
        latest_file = max(all_files, key=os.path.getctime)
        with open(latest_file, 'r') as f:
            for line in f.readlines():
                if "Average FPS:" in line:
                    value = re.search("      Average FPS:\t(.*)", line).group(1)
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
        results['preset'] = str(self._preset)
        results['avg_fps'] = str(self.get_avg_fps())
        results['min_fps'] = str(self.get_min_fps())
        results['max_fps'] = str(self.get_max_fps())
        results['iterations'] = str(self._iterations)
        return results

    def print_results(self):
        print(json.dumps(self.get_results()))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Strange Brigade benchmark")
    parser.add_argument('--proton', type=str, default="4.2")
    parser.add_argument('--iterations', type=int, default=3)
    parser.add_argument('--resolution', type=str, default='1920x1080',
                        choices=['1920x1080', '2560x1440', '3840x2160'])
    parser.add_argument('--preset', type=Brigade_preset,
                        default=Brigade_preset.HIGH,
                        choices=list(Brigade_preset))
    args = parser.parse_args(sys.argv[1:])

    brigade = Brigade(args.proton, args.resolution, args.preset, args.iterations)
    brigade.install()
    brigade.bench()
    brigade.print_results()
