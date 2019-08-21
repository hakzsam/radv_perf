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

##
# GTAV benchmark.
##
class GTAV_preset(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    def __str__(self):
        return self.value

class GTAV(SteamBenchmark):
    def __init__(self, proton, resolution, preset, iterations):
        SteamBenchmark.__init__(self, "GTAV")
        self._game_path = self._steam_dir + "/steamapps/common/Grand Theft Auto V"
        self._conf_path = self._steam_dir + "/steamapps/compatdata/271590"
        self._proton = proton
        self._preset = preset
        self._resolution = resolution
        self._iterations = iterations
        self._fps = []

    def install(self):
        pass

    def get_conf_options(self):
        conf = {}
        n = self._resolution.find('x')
        conf['width'] = self._resolution[:n]
        conf['height'] = self._resolution[n+1:]
        if self._preset == GTAV_preset.HIGH:
            conf['anisotropicQualityLevel'] = '16'
            conf['fogVolumes'] = ''
            conf['fxaa'] = '3'
            conf['grassQuality'] = '5'
            conf['lodScale'] = '1.0f'
            conf['multiSample'] = 8
            conf['particleQuality'] = '2'
            conf['particleShadows'] = ''
            conf['pedLodBias'] = '1.0f'
            conf['postFX'] = '3'
            conf['reflectionBlur'] = ''
            conf['reflectionQuality'] = '3'
            conf['SSA'] = ''
            conf['SSAO'] = '2'
            conf['shadowLongShadows'] = ''
            conf['shadowQuality'] = '3'
            conf['tessellation'] = '3'
            conf['textureQuality'] = '2'
            conf['txaa'] = ''
            conf['vehicleLodBias'] = '1.0f'
            conf['waterQuality'] = '1'
        elif self._preset == GTAV_preset.MEDIUM:
            conf['anisotropicQualityLevel'] = '0'
            conf['fogVolumes'] = ''
            conf['fxaa'] = '2'
            conf['grassQuality'] = '3'
            conf['lodScale'] = '0.0f'
            conf['multiSample'] = 2
            conf['particleQuality'] = '1'
            conf['particleShadows'] = ''
            conf['pedLodBias'] = '0.0f'
            conf['postFX'] = '2'
            conf['reflectionBlur'] = ''
            conf['reflectionQuality'] = '1'
            conf['SSA'] = ''
            conf['SSAO'] = '1'
            conf['shaderQuality'] = '1'
            conf['shadowLongShadows'] = ''
            conf['shadowQuality'] = '2'
            conf['tessellation'] = '1'
            conf['textureQuality'] = '1'
            conf['txaa'] = ''
            conf['vehicleLodBias'] = '0.0f'
            conf['waterQuality'] = '0'
        elif self._preset == GTAV_preset.LOW:
            conf['anisotropicQualityLevel'] = '0'
            #conf['fogVolumes'] = ''
            conf['fxaa'] = '0'
            conf['grassQuality'] = '0'
            conf['lodScale'] = '0.0f'
            conf['multiSample'] = 1
            conf['particleQuality'] = '0'
            #conf['particleShadows'] = ''
            conf['pedLodBias'] = '0.0f'
            conf['postFX'] = '0'
            #conf['reflectionBlur'] = ''
            conf['reflectionQuality'] = '0'
            #conf['SSA'] = ''
            conf['SSAO'] = '0'
            conf['shaderQuality'] = '0'
            #conf['shadowLongShadows'] = ''
            conf['shadowQuality'] = '0'
            conf['tessellation'] = '0'
            conf['textureQuality'] = '0'
            #conf['txaa'] = ''
            conf['vehicleLodBias'] = '0.0f'
            conf['waterQuality'] = '0'
        opts = []
        for k,v in conf.items():
            opts.append('-' + k + ' ' + str(v))
        return opts

    def run(self):
        olddir = os.getcwd()
        os.chdir(self._game_path)

        proton_dir = self._steam_dir + '/steamapps/common/Proton %s/' % self._proton
        cmd = [proton_dir + 'proton', 'run', './GTAVLauncher.exe',
               '-benchmark',
               '-DX11',
               '-benchmarknoaudio',
               '-fullscreen',
               '-ignoreDifferentVideoCard',
              ]
        cmd = cmd + self.get_conf_options()
        os.environ['STEAM_COMPAT_DATA_PATH'] = self._conf_path
        os.environ['SteamAppId'] = str(271590)
        self.run_process(cmd)
        time.sleep(3) # Not sure why this is needed.

        os.chdir(olddir)

    def bench(self):
        for i in range(0, self._iterations):
            self.run()
            self._fps.append(self.get_fps())

    def get_fps_for_scene(self, name):
        log_path = self._conf_path + "/pfx/drive_c/users/steamuser/My Documents/Rockstar Games/GTA V/Benchmarks"
        all_files = glob.glob(log_path + "/Benchmark-*.txt")
        # Get the latest file and extract the average number of FPS.
        latest_file = max(all_files, key=os.path.getctime)
        with open(latest_file, 'r') as f:
            inside_fps_block = False
            for line in f.readlines():
                if line.startswith("Frames Per Second"):
                    inside_fps_block = True
                if line.startswith("Time in milliseconds"):
                    inside_fps_block = False

                if inside_fps_block:
                    if line.startswith("Pass " + name):
                        # Pass 0, 0.257510, 112.171761, 38.383133
                        value = re.search('Pass ' + name + ', (.*), (.*), (.*)', line).group(3)
                        return round_fps(value)
        return 0

    def get_fps(self):
        fps = {}
        fps["scene-0"] = self.get_fps_for_scene("0")
        fps["scene-1"] = self.get_fps_for_scene("1")
        fps["scene-2"] = self.get_fps_for_scene("2")
        fps["scene-3"] = self.get_fps_for_scene("3")
        fps["scene-4"] = self.get_fps_for_scene("4")
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
        self.print_result("scene-0")
        self.print_result("scene-1")
        self.print_result("scene-2")
        self.print_result("scene-3")
        self.print_result("scene-4")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GTAV benchmark")
    parser.add_argument('--proton', type=str, default="4.2")
    parser.add_argument('--iterations', type=int, default=3)
    parser.add_argument('--dry-run', type=int, default=1)
    parser.add_argument('--resolution', type=str, default='1920x1080',
                        choices=['1920x1080', '2560x1440', '3840x2160'])
    parser.add_argument('--preset', type=GTAV_preset,
                        default=GTAV_preset.HIGH,
                        choices=list(GTAV_preset))
    args = parser.parse_args(sys.argv[1:])

    gtav = GTAV(args.proton, args.resolution, args.preset, args.iterations)
    gtav.install()
    if args.dry_run:
        gtav.run() # For compiling pipelines
    gtav.bench()
    gtav.print_results()
