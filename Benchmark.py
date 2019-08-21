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

    def run_process(self, cmd, stdout = DEVNULL, stderr = DEVNULL):
        process = subprocess.Popen(cmd, stderr=stderr, stdout=stdout)
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

class SteamBenchmark(Benchmark):
    def __init__(self, name):
        Benchmark.__init__(self, name)
        assert('STEAM_DIR' in os.environ)
        self._steam_dir = os.environ['STEAM_DIR']
