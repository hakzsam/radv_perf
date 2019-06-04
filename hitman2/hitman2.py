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
# Hitman2 benchmark.
##
class Hitman2_preset(Enum):
    LOW = "low"
    MEDIUM = "medium"
    ULTRA = "ultra"
    def __str__(self):
        return self.value

class Hitman2(Benchmark):
    def __init__(self, proton, resolution, preset, iterations):
        Benchmark.__init__(self, "Hitman2")
        self._game_path = STEAM_DIR + "/steamapps/common/HITMAN2"
        self._conf_path = STEAM_DIR + "/steamapps/compatdata/863550"
        self._proton = proton
        self._preset = preset
        self._resolution = resolution
        self._iterations = iterations
        self._fps = []

    def get_options(self):
        n = self._resolution.find('x')
        width = self._resolution[:n]
        height = self._resolution[n+1:]

        args = ['-SKIP_LAUNCHER',
                '-ao', 'START_BENCHMARK', 'true',
                '-ao', 'BENCHMARK_SCENE_INDEX', '1',
                '-ao', 'AUTO_QUIT_ENGINE', '120', 
                '-ao', 'FullScreen', '1',
                '-ao', 'RESOLUTION', width, 'x', height,
                'ConsoleCmd', 'UI_ShowProfileData', '1',
                'ConsoleCmd', 'EnableFPSLimiter', '0', 
                'ConsoleCmd', 'settings_vsync', '0',
                'ConsoleCmd', 'settings_SetHDR', '0']

        if self._preset == Hitman2_preset.LOW:
            gfx_opts = ['ConsoleCmd', 'settings_SetDetailLOD', '0',
                        'ConsoleCmd', 'settings_SetAntialiasing', '0',
                        'ConsoleCmd', 'settings_SetTextureQuality', '0',
                        'ConsoleCmd', 'settings_SetTextureFilter', '0',
                        'ConsoleCmd', 'settings_SetSSAO', '0',
                        'ConsoleCmd', 'settings_SetShadowResolution', '0']
        elif self._preset == Hitman2_preset.MEDIUM:
            gfx_opts = ['ConsoleCmd', 'settings_SetDetailLOD', '1',
                        'ConsoleCmd', 'settings_SetAntialiasing', '2',
                        'ConsoleCmd', 'settings_SetTextureQuality', '1',
                        'ConsoleCmd', 'settings_SetTextureFilter', '1',
                        'ConsoleCmd', 'settings_SetSSAO', '1',
                        'ConsoleCmd', 'settings_SetShadowResolution', '1']
        else:
            gfx_opts = ['ConsoleCmd', 'settings_SetDetailLOD', '3',
                        'ConsoleCmd', 'settings_SetAntialiasing', '2',
                        'ConsoleCmd', 'settings_SetTextureQuality', '2',
                        'ConsoleCmd', 'settings_SetTextureFilter', '3',
                        'ConsoleCmd', 'settings_SetSSAO', '1',
                        'ConsoleCmd', 'settings_SetShadowResolution', '2']
        return args + gfx_opts

    def run(self):
        olddir = os.getcwd()
        os.chdir(self._game_path + "/Retail")

        proton_dir = STEAM_DIR + '/steamapps/common/Proton %s/' % self._proton
        cmd = [proton_dir + 'proton', 'run', './HITMAN2.exe']
        cmd += self.get_options()
        os.environ['STEAM_COMPAT_DATA_PATH'] = self._conf_path
        os.environ['SteamAppId'] = str(863550)
        self.run_process(cmd)
        time.sleep(3) # Not sure why this is needed.

        os.chdir(olddir)

    def bench(self):
        for i in range(0, self._iterations):
            self.run()
            self._fps.append(self.get_fps())

    def get_fps(self):
        log_path = self._conf_path + "/pfx/drive_c/users/steamuser/hitman/"
        all_files = glob.glob(log_path + "/profiledata.txt")
        # Get the latest file and extract the average number of FPS.
        latest_file = max(all_files, key=os.path.getctime)
        with open(latest_file, 'r') as f:
            in_fps_block = False
            for line in f.readlines():
                if in_fps_block:
                    if "Average" in line:
                        value = re.search("(.*)fps Average", line).group(1)
                        return round_fps(value)
                if "---- CPU ----":
                    in_fps_block = True
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
    parser = argparse.ArgumentParser(description="Hitman2 benchmark")
    parser.add_argument('--proton', type=str, default="4.2")
    parser.add_argument('--iterations', type=int, default=3)
    parser.add_argument('--dry-run', type=int, default=1)
    parser.add_argument('--resolution', type=str, default='1920x1080',
                        choices=['1920x1080', '2560x1440', '3840x2160'])
    parser.add_argument('--preset', type=Hitman2_preset,
                        default=Hitman2_preset.ULTRA,
                        choices=list(Hitman2_preset))
    args = parser.parse_args(sys.argv[1:])

    hitman2 = Hitman2(args.proton, args.resolution, args.preset, args.iterations)
    if args.dry_run:
        hitman2.run() # For compiling pipelines
    hitman2.bench()
    hitman2.print_results()
