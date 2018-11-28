#!/bin/python

import argparse
import glob
import os
import shutil
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), ".."))

from enum import Enum
from Benchmark import *
from Util import *

##
# A Total War Saga: THRONES OF BRITANNIA benchmark.
##
class ToB_preset(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    ULTRA = "ultra"
    EXTREME = "extreme"
    def __str__(self):
        return self.value

class ToB(Benchmark):
    def __init__(self, resolution, preset, iterations):
        Benchmark.__init__(self, "ToB")
        self._game_path = os.environ['HOME'] + "/work/Steam/steamapps/common/Total War Saga Thrones of Britannia"
        self._conf_path = os.environ['HOME'] + "/.local/share/feral-interactive/Thrones of Britannia/"
        self._log_path = self._conf_path + "VFS/User/AppData/Roaming/The Creative Assembly/ThronesofBritannia/benchmarks/"
        self._resolution = resolution
        self._preset = preset
        self._iterations = iterations
        self._fps = []

    def get_config_file(self):
        dirname = os.path.dirname(os.path.realpath(__file__))
        return dirname + "/preferences.xml"

    def install(self):
        conf = {}
        n = self._resolution.find('x')
        conf['@ScreenW@']=self._resolution[:n]
        conf['@ScreenH@']=self._resolution[n+1:]
        if self._preset == ToB_preset.LOW:
            conf['@gfx_aa@']='0'
            conf['@gfx_building_quality@']='0'
            conf['@gfx_depth_of_field@']='0'
            conf['@gfx_distortion@']='0'
            conf['@gfx_effects_quality@']='0'
            conf['@gfx_fleet_size@']='0'
            conf['@gfx_grass_quality@']='0'
            conf['@gfx_screen_space_reflections@']='0'
            conf['@gfx_shadow_quality@']='0'
            conf['@gfx_sky_quality@']='0'
            conf['@gfx_ssao@']='0'
            conf['@gfx_terrain_quality@']='0'
            conf['@gfx_texture_filtering@']='0'
            conf['@gfx_texture_quality@']='2'
            conf['@gfx_tree_quality@']='0'
            conf['@gfx_unit_quality@']='0'
            conf['@gfx_unit_size@']='0'
            conf['@gfx_water_quality@']='0'
        elif self._preset == ToB_preset.MEDIUM:
            conf['@gfx_aa@']='0'
            conf['@gfx_building_quality@']='1'
            conf['@gfx_depth_of_field@']='0'
            conf['@gfx_distortion@']='1'
            conf['@gfx_effects_quality@']='1'
            conf['@gfx_fleet_size@']='1'
            conf['@gfx_grass_quality@']='1'
            conf['@gfx_screen_space_reflections@']='0'
            conf['@gfx_shadow_quality@']='1'
            conf['@gfx_sky_quality@']='1'
            conf['@gfx_ssao@']='0'
            conf['@gfx_terrain_quality@']='1'
            conf['@gfx_texture_filtering@']='0'
            conf['@gfx_texture_quality@']='2'
            conf['@gfx_tree_quality@']='1'
            conf['@gfx_unit_quality@']='1'
            conf['@gfx_unit_size@']='1'
            conf['@gfx_water_quality@']='1'
        elif self._preset == ToB_preset.HIGH:
            conf['@gfx_aa@']='0'
            conf['@gfx_building_quality@']='2'
            conf['@gfx_depth_of_field@']='0'
            conf['@gfx_distortion@']='1'
            conf['@gfx_effects_quality@']='2'
            conf['@gfx_fleet_size@']='2'
            conf['@gfx_grass_quality@']='2'
            conf['@gfx_screen_space_reflections@']='1'
            conf['@gfx_shadow_quality@']='2'
            conf['@gfx_sky_quality@']='2'
            conf['@gfx_ssao@']='0'
            conf['@gfx_terrain_quality@']='2'
            conf['@gfx_texture_filtering@']='0'
            conf['@gfx_texture_quality@']='2'
            conf['@gfx_tree_quality@']='2'
            conf['@gfx_unit_quality@']='2'
            conf['@gfx_unit_size@']='2'
            conf['@gfx_water_quality@']='2'
        elif self._preset == ToB_preset.ULTRA:
            conf['@gfx_aa@']='1'
            conf['@gfx_building_quality@']='3'
            conf['@gfx_depth_of_field@']='0'
            conf['@gfx_distortion@']='1'
            conf['@gfx_effects_quality@']='3'
            conf['@gfx_fleet_size@']='2'
            conf['@gfx_grass_quality@']='3'
            conf['@gfx_screen_space_reflections@']='2'
            conf['@gfx_shadow_quality@']='3'
            conf['@gfx_sky_quality@']='3'
            conf['@gfx_ssao@']='1'
            conf['@gfx_terrain_quality@']='3'
            conf['@gfx_texture_filtering@']='1'
            conf['@gfx_texture_quality@']='2'
            conf['@gfx_tree_quality@']='3'
            conf['@gfx_unit_quality@']='3'
            conf['@gfx_unit_size@']='2'
            conf['@gfx_water_quality@']='3'
        elif self._preset == ToB_preset.EXTREME:
            conf['@gfx_aa@']='3'
            conf['@gfx_building_quality@']='3'
            conf['@gfx_depth_of_field@']='1'
            conf['@gfx_distortion@']='1'
            conf['@gfx_effects_quality@']='3'
            conf['@gfx_fleet_size@']='2'
            conf['@gfx_grass_quality@']='3'
            conf['@gfx_screen_space_reflections@']='2'
            conf['@gfx_shadow_quality@']='3'
            conf['@gfx_sky_quality@']='3'
            conf['@gfx_ssao@']='1'
            conf['@gfx_terrain_quality@']='3'
            conf['@gfx_texture_filtering@']='2'
            conf['@gfx_texture_quality@']='2'
            conf['@gfx_tree_quality@']='3'
            conf['@gfx_unit_quality@']='3'
            conf['@gfx_unit_size@']='3'
            conf['@gfx_water_quality@']='3'

        conf_file = get_file_contents(self.get_config_file())
        for k,v in conf.items():
            conf_file = conf_file.replace(k, v)
        olddir = os.getcwd()
        os.chdir(self._conf_path)
        with open(self._conf_path + "preferences", 'w+') as f:
            f.write(conf_file)
        os.chdir(olddir)

    def run(self):
        olddir = os.getcwd()
        os.chdir(self._game_path + "/bin")
        self.run_process(["./ThronesOfBritannia", "-benchmark", "basic_benchmark.xml"])
        os.chdir(olddir)

    def bench(self):
        for i in range(0, self._iterations):
            self.run()
            self._fps.append(self.get_fps())

    def get_fps(self):
        all_files = glob.glob(self._log_path + "/benchmark_*")
        list_of_files = []
        # Exclude some files.
        for f in all_files:
            if not "frametimes" in f:
                list_of_files.append(f)
        # Get the latest file and extract the average number of FPS.
        latest_file = max(list_of_files, key=os.path.getctime)
        with open(latest_file, 'r') as f:
            in_fps_block = False
            for line in f.readlines():
                if in_fps_block:
                    if "mean" in line:
                        value = re.search("mean (.*)", line).group(1)
                        return round_fps(value)
                if "frames per second" in line:
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
        print(self.get_results())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ToB benchmark")
    parser.add_argument('--iterations', type=int, default=3)
    parser.add_argument('--resolution', type=str, default='1920x1080',
                        choices=['1920x1080', '2560x1440', '3840x2160'])
    parser.add_argument('--preset', type=ToB_preset,
                        default=ToB_preset.EXTREME,
                        choices=list(ToB_preset))
    args = parser.parse_args(sys.argv[1:])

    tob = ToB(args.resolution, args.preset, args.iterations)
    tob.install()
    tob.bench()
    tob.print_results()
