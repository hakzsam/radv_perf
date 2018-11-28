#!/bin/python

import os
import re
import sys
import getopt
import subprocess
import time
import tempfile

from subprocess import DEVNULL
from subprocess import check_output

def round_fps(fps):
    return round(float(fps), 2)

##
# Base class for all benchmarks.
##
class Benchmark:
    def __init__(self, name):
        self.name = name
        self.num_results = 1

    def run_process(self, cmd, logfile = DEVNULL):
        process = subprocess.Popen(cmd)
        process.wait()
        return process

    def get_latest_file(self, path):
        files = os.listdir(path)
        paths = [os.path.join(path, basename) for basename in files]
        return max(paths, key=os.path.getctime)

    def skip_first_run(self):
        return True

    def get_num_results(self):
        return self.num_results

    def get_name(self):
        return self.name

##
# Serious Sam 2017 benchmark.
##
class Sam2017(Benchmark):
    def __init__(self):
        Benchmark.__init__(self, "Sam2017")
        self.log_path = os.environ['HOME'] + "/.steam/steam/steamapps/common/Serious Sam Fusion 2017/Log/"

    def getpid(self, name):
        return int(check_output(["pidof", "-s", name]))

    def run(self):
        self.run_process(["steam", "-applaunch", "564310", "+exec", "pts-tfe-fusion-run.lua"])

        # Wait to be sure the application is started.
        self.run_process(["sleep", "5"])

        # Get PID.
        pid = self.getpid("Sam2017")

        # Wait until the process is done.
        while os.path.exists("/proc/%s" % str(pid)):
            time.sleep(1)

    def get_avg_fps(self):
        log_file = self.log_path + "/Sam2017.log"
        with open(log_file, "r") as f:
            for line in f:
                if "Average" in line:
                    value = re.search('Average: (.*) FPS', line).group(1)
                    return round_fps(value)
        return 0

##
# MadMax benchmark.
##
class MadMax(Benchmark):
    def __init__(self):
        Benchmark.__init__(self, "MadMax")
        self.game_path = os.environ['HOME'] + "/work/Steam/steamapps/common/Mad Max"
        self.log_path = os.environ['HOME'] + "/.local/share/feral-interactive/Mad Max/VFS/User/AppData/Roaming/WB Games/Mad Max/FeralBenchmark"

    def get_num_results(self):
        return 4 # MadMax has 4 scenes

    def run(self):
        os.chdir(self.game_path + "/bin")
        self.run_process(["./MadMax", "-feral-benchmark"])

    def get_avg_fps(self):
        log_dir = self.get_latest_file(self.log_path)
        fps = []
        for i in range(1, 5):
            log_file = log_dir + "/benchmark_" + str(i) + ".xml"
            with open(log_file, "r") as f:
                for line in f:
                    if "avg_fps" in line:
                        value = re.search('<value name="avg_fps">(.*)</value>', line).group(1)
                        value = round_fps(value)
                        fps.append(value)
        return fps

class BenchmarkFactory:
    def get(self, name):
        elif name == "sam2017":
            return Sam2017()
        elif name == "madmax":
            return MadMax()
        else:
            sys.exit("Invalid benchmark name!")

def print_info():
        glxinfo = check_output(["glxinfo"])
        for line in glxinfo.decode().split('\n'):
            if "OpenGL renderer string:" in line:
                print(line)
            if "OpenGL core profile version string:" in line:
                print(line)
        if os.environ.get('RADV_DEBUG') != None:
            print("RADV_DEBUG: " + os.environ['RADV_DEBUG'])
        if os.environ.get('RADV_PERFTEST') != None:
            print("RADV_PERFTEST: " + os.environ['RADV_PERFTEST'])
        no_turbo = int(check_output(["cat", "/sys/devices/system/cpu/intel_pstate/no_turbo"]))
        if no_turbo == 0:
            print("Warning: CPU turbo mode is enabled!")

        kernel_version = check_output(["uname", "-r"])
        print("Kernel: " + str(kernel_version.decode("utf-8")))

def main(argv):
    num_run = 1 # One run by default
    skip_first_run = True

    try:
        opts, args = getopt.getopt(argv, "hn:s", ["help, bench=, run=, skip="])
    except getopt.GetOptError:
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-n":
            num_run = arg
        elif opt == "-s":
            skip_first_run = False

    if len(args) == 0:
        sys.exit("Missing benchmarks?")

    print_info()

    # Do it!
    for name in args:
        b = BenchmarkFactory().get(name)

        # Do a dry-run for compiling shaders and throw away the result.
        if b.skip_first_run() and skip_first_run == True:
            b.run()

        fps = []
        for n in range(0, int(num_run)):
            b.run()
            fps.append(b.get_avg_fps())

        if b.get_num_results() > 1:
            for i in range(0, b.get_num_results()):
                tmp_fps = []
                for j in range(0, int(num_run)):
                    tmp_fps.append(fps[j][i])
                avg_fps = round_fps(sum(tmp_fps) / int(num_run))
                min_fps = min(tmp_fps)
                max_fps = max(tmp_fps)
                print(b.get_name() + " #" + str(i) + " (avg: " + str(avg_fps) + ", min: " + str(min_fps) + ", max: " + str(max_fps) + ")")
        else:
            avg_fps = round_fps(sum(fps) / int(num_run))
            min_fps = min(fps)
            max_fps = max(fps)
            print(b.get_name() + " (avg: " + str(avg_fps) + ", min: " + str(min_fps) + ", max: " + str(max_fps) + ")")

if __name__ == "__main__":
    main(sys.argv[1:])
