#!/bin/python3

import os
import sys
import time
import glob
import argparse
import csv
import signal
import xml.etree.ElementTree as ET
import io

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), ".."))

from enum import Enum
from Benchmark import *
from Util import *

def getpid(name):
    return int(check_output(["pidof", "-s", name]))

##
# Shadow of The Tomb Raider benchmark.
##
class SOTR_preset(Enum):
    LOWEST = "Lowest"
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    VERY_HIGH = "VeryHigh"
    def __str__(self):
        return self.value

class SOTR_antialiasing(Enum):
    OFF = "off"
    SMAA = "taa"
    TAA = "smaa"
    SMAA_T2X = "smaa_t2x"
    def __str__(self):
        return self.value

class SOTR(SteamBenchmark):
    def __init__(self, resolution, preset, antialiasing, iterations):
        SteamBenchmark.__init__(self, "SotTR")
        self._game_path = self._steam_dir + "/steamapps/common/Shadow of the Tomb Raider"
        self._conf_path = os.environ['HOME'] + "/.local/share/feral-interactive/Shadow of the Tomb Raider/"
        self._resolution = resolution
        self._preset = preset
        self._antialiasing = antialiasing
        self._iterations = iterations
        self._fps = []

    def get_config_file(self):
        dirname = os.path.dirname(os.path.realpath(__file__))
        return dirname + "/preferences.xml"

    def convert_antialiasing(self):
        if self._antialiasing == SOTR_antialiasing.OFF:
            return 0
        elif self._antialiasing == SOTR_antialiasing.SMAA:
            return 1
        elif self._antialiasing == SOTR_antialiasing.TAA:
            return 2
        elif self._antialiasing == SOTR_antialiasing.SMAA_T2X:
            return 3

    def install(self):
        # setup environment
        os.environ['STEAM_RUNTIME'] = '0'

        olddir = os.getcwd()

        # run launcher to get the device name and some magic settings so that AA
        # and resolution can be configured
        with open(self._conf_path + "preferences", 'w+') as f:
            f.write('')

        os.chdir(self._game_path)
        process = subprocess.Popen("./ShadowOfTheTombRaider.sh", stderr=DEVNULL, stdout=DEVNULL)
        time.sleep(5)
        process.terminate()
        pid = getpid("ShadowOfTheTombRaider")
        os.kill(pid, signal.SIGTERM)

        os.chdir(olddir)

        tree = ET.ElementTree()
        tree.parse(self._conf_path + "preferences")
        setup = tree.find(".//key[@name='Setup']")
        magic = [elem for elem in setup.findall("value") if "SeenSpecificationAlertUUID" in elem.attrib["name"]]

        device_names = []
        for elem in magic:
            if "SeenSpecificationAlertUUIDHigh_Default" in elem.attrib["name"]:
                device_names.append(elem.attrib["name"].split("High_Default")[1])
        device_name = device_names[0] # sotr seems to use the first

        device_setup = setup.find("./key[@name='%s']" % device_name).findall("value")
        device_setup = [elem for elem in device_setup if elem.attrib["name"] not in ["ScreenW", "ScreenH", "FullScreen"]]

        # create preferences file
        conf = {}
        conf['device_name'] = device_name
        conf['magic'] = ''.join(ET.tostring(elem, encoding="unicode") for elem in magic)
        conf['device_setup'] = ''.join(ET.tostring(elem, encoding="unicode") for elem in device_setup)
        n = self._resolution.find('x')
        conf['ScreenW'] = self._resolution[:n]
        conf['ScreenH'] = self._resolution[n+1:]

        if self._antialiasing == SOTR_antialiasing.OFF:
            conf['gfx_aa'] = 0
        elif self._antialiasing == SOTR_antialiasing.SMAA:
            conf['gfx_aa'] = 1
        elif self._antialiasing == SOTR_antialiasing.TAA:
            conf['gfx_aa'] = 2
        elif self._antialiasing == SOTR_antialiasing.SMAA_T2X:
            conf['gfx_aa'] = 3

        if self._preset == SOTR_preset.LOWEST:
            conf['gfx_ao'] = 0
            conf['gfx_bloom'] = 0
            conf['gfx_dof_quality'] = 0
            conf['gfx_lod'] = 0
            conf['gfx_motion_blur'] = 0
            conf['gfx_contact_shadows'] = 0
            conf['gfx_preset'] = 0
            conf['gfx_reflections'] = 0
            conf['gfx_shadow_quality'] = 0
            conf['gfx_tessellation'] = 0
            conf['gfx_tex_filter'] = 0
            conf['gfx_tex_quality'] = 0
            conf['gfx_tressfx'] = 0
            conf['gfx_volumetric'] = 0
        elif self._preset == SOTR_preset.LOW:
            conf['gfx_ao'] = 0
            conf['gfx_bloom'] = 1
            conf['gfx_dof_quality'] = 0
            conf['gfx_lod'] = 1
            conf['gfx_motion_blur'] = 0
            conf['gfx_contact_shadows'] = 0
            conf['gfx_preset'] = 1
            conf['gfx_reflections'] = 0
            conf['gfx_shadow_quality'] = 1
            conf['gfx_tessellation'] = 0
            conf['gfx_tex_filter'] = 0
            conf['gfx_tex_quality'] = 0
            conf['gfx_tressfx'] = 0
            conf['gfx_volumetric'] = 1
        elif self._preset == SOTR_preset.MEDIUM:
            conf['gfx_ao'] = 1
            conf['gfx_bloom'] = 1
            conf['gfx_dof_quality'] = 1
            conf['gfx_lod'] = 2
            conf['gfx_motion_blur'] = 1
            conf['gfx_contact_shadows'] = 0
            conf['gfx_preset'] = 2
            conf['gfx_reflections'] = 1
            conf['gfx_shadow_quality'] = 1
            conf['gfx_tessellation'] = 0
            conf['gfx_tex_filter'] = 1
            conf['gfx_tex_quality'] = 1
            conf['gfx_tressfx'] = 1
            conf['gfx_volumetric'] = 1
        elif self._preset == SOTR_preset.HIGH:
            conf['gfx_ao'] = 1
            conf['gfx_bloom'] = 1
            conf['gfx_dof_quality'] = 1
            conf['gfx_lod'] = 2
            conf['gfx_motion_blur'] = 1
            conf['gfx_contact_shadows'] = 0
            conf['gfx_preset'] = 3
            conf['gfx_reflections'] = 1
            conf['gfx_shadow_quality'] = 2
            conf['gfx_tessellation'] = 1
            conf['gfx_tex_filter'] = 2
            conf['gfx_tex_quality'] = 2
            conf['gfx_tressfx'] = 1
            conf['gfx_volumetric'] = 1
        elif self._preset == SOTR_preset.VERY_HIGH:
            conf['gfx_ao'] = 1
            conf['gfx_bloom'] = 1
            conf['gfx_dof_quality'] = 2
            conf['gfx_lod'] = 3
            conf['gfx_motion_blur'] = 1
            conf['gfx_contact_shadows'] = 1
            conf['gfx_preset'] = 4
            conf['gfx_reflections'] = 1
            conf['gfx_shadow_quality'] = 3
            conf['gfx_tessellation'] = 1
            conf['gfx_tex_filter'] = 3
            conf['gfx_tex_quality'] = 3
            conf['gfx_tressfx'] = 1
            conf['gfx_volumetric'] = 1

        conf_file = get_file_contents(self.get_config_file())
        for k,v in conf.items():
            conf_file = conf_file.replace('@'+k+'@', str(v))

        with open(self._conf_path + "preferences", 'w+') as f:
            f.write(conf_file)

    def run(self):
        olddir = os.getcwd()
        os.chdir(self._game_path)
        cmd = ["./ShadowOfTheTombRaider.sh"]
        proc = self.run_process(cmd)
        os.chdir(olddir)

    def bench(self):
        for i in range(0, self._iterations):
            self.run()
            self._fps.append(self.get_fps())

    def get_fps_for_scene(self, name):
        list_of_files = glob.glob(self._conf_path + "SaveData/Shadow of the Tomb Raider_benchmarkresults_X_feral_" + name + "_*")
        # Get the latest file and compute the average number of FPS.
        latest_file = max(list_of_files, key=os.path.getctime)
        with open(latest_file, 'r') as f:
            # exclude first frame
            rows = list(csv.DictReader(f))[1:]
            frametimes = [float(row['Value']) for row in rows if row['EventType'] == 'frame_time_ms']
            return round_fps(1000.0 / (sum(frametimes) / len(frametimes)))
        return 0

    def get_fps(self):
        fps = {}
        fps["day_of_dead"] = self.get_fps_for_scene("dd_day_of_the_dead")
        fps["jungle"] = self.get_fps_for_scene("lj_lost_in_the_jungle")
        fps["paititi"] = self.get_fps_for_scene("pa_hub_paititi")
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
        result['antialiasing'] = str(self._antialiasing)
        result['scene'] = str(scene)
        result['avg_fps'] = str(avg_fps)
        result['min_fps'] = str(min_fps)
        result['max_fps'] = str(max_fps)
        result['interations'] = str(self._iterations)
        print(result)

    def print_results(self):
        self.print_result("day_of_dead")
        self.print_result("jungle")
        self.print_result("paititi")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Shadow Of The Tomb Raider benchmark")
    parser.add_argument('--iterations', type=int, default=3)
    parser.add_argument('--resolution', type=str, default='1920x1080',
                        choices=['1920x1080', '2560x1440', '3840x2160'])
    parser.add_argument('--preset', type=SOTR_preset,
                        default=SOTR_preset.VERY_HIGH,
                        choices=list(SOTR_preset))
    parser.add_argument('--antialiasing', type=SOTR_antialiasing,
                        default=SOTR_antialiasing.TAA,
                        choices=list(SOTR_antialiasing))
    args = parser.parse_args(sys.argv[1:])

    sotr = SOTR(args.resolution, args.preset, args.antialiasing, args.iterations)
    sotr.install()
    sotr.bench()
    sotr.print_results()
