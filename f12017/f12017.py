#!/bin/python

import argparse
import os
import shutil
import sys

from enum import Enum

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), ".."))

from Benchmark import *
from Util import *

##
# F12017 benchmark.
##
class F12017_preset(Enum):
    ULTRA_LOW = "ultralow"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    ULTRA_HIGH = "ultrahigh"
    def __str__(self):
        return self.value

class F12017_antialiasing(Enum):
    OFF = "off"
    TAA_CHECKERBOARD = "taa+checkerboard"
    TAA = "taa"
    def __str__(self):
        return self.value

class F12017(Benchmark):
    def __init__(self, resolution, preset, antialiasing, iterations):
        Benchmark.__init__(self, "F12017")
        self._game_path = os.environ['HOME'] + "/work/Steam/steamapps/common/F1 2017"
        self._conf_path = os.environ['HOME'] + "/.local/share/feral-interactive/F1 2017/"
        self._log_path = os.environ['HOME'] + "/.local/share/feral-interactive/F1 2017/SaveData/feral_bench"
        self._resolution = resolution
        self._preset = preset
        self._antialiasing = antialiasing
        self._iterations = iterations
        self._fps = []

    def get_config_file(self):
        dirname = os.path.dirname(os.path.realpath(__file__))
        return dirname + "/preferences.xml"

    def install(self):
        conf = {}
        n = self._resolution.find('x')
        conf['resolution_width']=self._resolution[:n]
        conf['resolution_height']=self._resolution[n+1:]
        conf['antialiasing']=str(self._antialiasing)
        if self._preset == F12017_preset.ULTRA_LOW:
            conf['advanced_smoke_shadows']='off'
            conf['ambient_occlusion']='off'
            conf['crowd']='low'
            conf['dynamic_hair']='low'
            conf['ground_cover']='low'
            conf['hdr_mode']='0'
            conf['lighting']='low'
            conf['mirrors']='low'
            conf['particles']='off'
            conf['postprocess']='low'
            conf['screen_space_reflections']='off'
            conf['shadows']='low'
            conf['skidmarks']='off'
            conf['skidmarks_blending']='off'
            conf['smoke_shadows']='off'
            conf['ssrt_shadows']='off'
            conf['texture_streaming']='ultralow'
            conf['vehicle_reflections']='ultralow'
            conf['weather_effects']='low'
        elif self._preset == F12017_preset.LOW:
            conf['advanced_smoke_shadows']='off'
            conf['ambient_occlusion']='off'
            conf['crowd']='low'
            conf['dynamic_hair']='low'
            conf['ground_cover']='low'
            conf['hdr_mode']='0'
            conf['lighting']='low'
            conf['mirrors']='low'
            conf['particles']='low'
            conf['postprocess']='low'
            conf['screen_space_reflections']='off'
            conf['shadows']='low'
            conf['skidmarks']='off'
            conf['skidmarks_blending']='off'
            conf['smoke_shadows']='low'
            conf['ssrt_shadows']='off'
            conf['texture_streaming']='low'
            conf['vehicle_reflections']='low'
            conf['weather_effects']='low'
        elif self._preset == F12017_preset.MEDIUM:
            conf['advanced_smoke_shadows']='off'
            conf['ambient_occlusion']='off'
            conf['crowd']='low'
            conf['dynamic_hair']='high'
            conf['ground_cover']='medium'
            conf['hdr_mode']='0'
            conf['lighting']='medium'
            conf['mirrors']='medium'
            conf['particles']='medium'
            conf['postprocess']='medium'
            conf['screen_space_reflections']='medium'
            conf['shadows']='medium'
            conf['skidmarks']='low'
            conf['skidmarks_blending']='off'
            conf['smoke_shadows']='low'
            conf['ssrt_shadows']='off'
            conf['texture_streaming']='medium'
            conf['vehicle_reflections']='medium'
            conf['weather_effects']='medium'
        elif self._preset == F12017_preset.HIGH:
            conf['advanced_smoke_shadows']='off'
            conf['ambient_occlusion']='on'
            conf['crowd']='high'
            conf['dynamic_hair']='high'
            conf['ground_cover']='high'
            conf['hdr_mode']='0'
            conf['lighting']='high'
            conf['mirrors']='high'
            conf['particles']='high'
            conf['postprocess']='high'
            conf['screen_space_reflections']='high'
            conf['shadows']='high'
            conf['skidmarks']='high'
            conf['skidmarks_blending']='off'
            conf['smoke_shadows']='high'
            conf['ssrt_shadows']='off'
            conf['texture_streaming']='high'
            conf['vehicle_reflections']='high'
            conf['weather_effects']='high'
        elif self._preset == F12017_preset.ULTRA_HIGH:
            conf['advanced_smoke_shadows']='off'
            conf['ambient_occlusion']='hbao'
            conf['crowd']='high'
            conf['dynamic_hair']='high'
            conf['ground_cover']='ultra'
            conf['hdr_mode']='0'
            conf['lighting']='high'
            conf['mirrors']='ultra'
            conf['particles']='high'
            conf['postprocess']='high'
            conf['screen_space_reflections']='ultra'
            conf['shadows']='ultra'
            conf['skidmarks']='high'
            conf['skidmarks_blending']='off'
            conf['smoke_shadows']='high'
            conf['ssrt_shadows']='off'
            conf['texture_streaming']='ultra'
            conf['vehicle_reflections']='ultra'
            conf['weather_effects']='ultra'

        conf_file = get_file_contents(self.get_config_file())
        conf_file = conf_file.replace('RESOLUTION_WIDTH', conf['resolution_width'])
        conf_file = conf_file.replace('RESOLUTION_HEIGHT', conf['resolution_height'])
        conf_file = conf_file.replace('ANTIALIASING', conf['antialiasing'])
        conf_file = conf_file.replace('ADVANCED_SMOKE_SHADOWS', conf['advanced_smoke_shadows'])
        conf_file = conf_file.replace('AMBIENT_OCCLUSION', conf['ambient_occlusion'])
        conf_file = conf_file.replace('CROWD', conf['crowd'])
        conf_file = conf_file.replace('DYNAMIC_HAIR', conf['dynamic_hair'])
        conf_file = conf_file.replace('GROUND_COVER', conf['ground_cover'])
        conf_file = conf_file.replace('HDR_MODE', conf['hdr_mode'])
        conf_file = conf_file.replace('LIGHTING', conf['lighting'])
        conf_file = conf_file.replace('MIRRORS', conf['mirrors'])
        conf_file = conf_file.replace('PARTICLES', conf['particles'])
        conf_file = conf_file.replace('POSTPROCESS', conf['postprocess'])
        conf_file = conf_file.replace('SCREEN_SPACE_REFLECTIONS', conf['screen_space_reflections'])
        conf_file = conf_file.replace('SMOKE_SHADOWS', conf['smoke_shadows'])
        conf_file = conf_file.replace('SSRT_SHADOWS', conf['ssrt_shadows'])
        conf_file = conf_file.replace('SHADOWS', conf['shadows'])
        conf_file = conf_file.replace('SKIDMARKS_BLENDING', conf['skidmarks_blending'])
        conf_file = conf_file.replace('SKIDMARKS', conf['skidmarks'])
        conf_file = conf_file.replace('TEXTURE_STREAMING', conf['texture_streaming'])
        conf_file = conf_file.replace('VEHICLE_REFLECTIONS', conf['vehicle_reflections'])
        conf_file = conf_file.replace('WEATHER_EFFECTS', conf['weather_effects'])
        olddir = os.getcwd()
        os.chdir(self._conf_path)
        with open(self._conf_path + "preferences", 'w+') as f:
            f.write(conf_file)
        os.chdir(olddir)

    def run(self):
        olddir = os.getcwd()
        os.chdir(self._game_path + "/bin")
        self.run_process(["./F12017", "-benchmark", "basic_benchmark.xml"])
        os.chdir(olddir)

    def bench(self):
        for i in range(0, self._iterations):
            self.run()
            self._fps.append(self._get_fps())

    def _get_fps(self):
        log_file = self.get_latest_file(self._log_path)
        with open(log_file, "r") as f:
            for line in f:
                if "avg_fps" in line:
                    value = re.search('avg_fps="(.*)" avg_', line).group(1)
                    return round_fps(value)
        return 0

    def get_min_fps(self):
        return min(self._fps)

    def get_max_fps(self):
        return max(self._fps)

    def get_avg_fps(self):
        return sum(self._fps) / self._iterations

    def print_results(self):
        results = {}
        results['resolution'] = str(self._resolution)
        results['preset'] = str(self._preset)
        results['antialiasing'] = str(self._antialiasing)
        results['avg_fps'] = str(self.get_avg_fps())
        results['min_fps'] = str(self.get_min_fps())
        results['max_fps'] = str(self.get_max_fps())
        results['iterations'] = str(self._iterations)
        print(results)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="F12017 benchmark")
    parser.add_argument('--iterations', type=int, default=3)
    parser.add_argument('--resolution', type=str, default='1920x1080',
                        choices=['1920x1080', '2560x1440', '3840x2160'])
    parser.add_argument('--preset', type=F12017_preset,
                        default=F12017_preset.ULTRA_HIGH,
                        choices=list(F12017_preset))
    parser.add_argument('--antialiasing', type=F12017_antialiasing,
                        default=F12017_antialiasing.OFF,
                        choices=list(F12017_antialiasing))
    args = parser.parse_args(sys.argv[1:])

    f12017 = F12017(args.resolution, args.preset, args.antialiasing, args.iterations)
    f12017.install()
    f12017.bench()
    f12017.print_results()
