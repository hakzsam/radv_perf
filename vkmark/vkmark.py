#!/bin/python

import argparse
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), ".."))

from Benchmark import *

##
# Vkmark benchmark.
##
class Vkmark(Benchmark):
    def __init__(self, num_iterations, size):
        Benchmark.__init__(self, "Vkmark")
        self._path = os.environ['HOME'] + "/programming/vkmark"
        self._num_iterations = num_iterations
        self._size = size
        self._scores = []

    def _get_score(self, logfile):
        with open(logfile) as f:
            for line in f:
                if "vkmark Score:" in line:
                    value = re.search('vkmark Score:(.*)', line).group(1)
                    return round_fps(value.strip())
        return 0

    def bench(self):
        olddir = os.getcwd()
        os.chdir(self._path + "/build")
        for i in range(0, self._num_iterations):
            logfile = tempfile.mktemp()
            stdout = open(logfile, "w+")
            cmd = ["src/vkmark",
                   "--winsys-dir=src",
                   "--data-dir=../data",
                   "--size=" + self._size]
            self.run_process(cmd, stdout)
            self._scores.append(self._get_score(logfile))
        os.chdir(olddir)

    def get_min_score(self):
        return min(self._scores)

    def get_max_score(self):
        return max(self._scores)

    def get_avg_score(self):
        return sum(self._scores) / self._num_iterations

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Vkmark benchmark")
    parser.add_argument('--iterations', type=int, default=1)
    parser.add_argument('--resolution', type=str, default='1920x1080',
                        choices=['1920x1080', '2560x1440', '3840x2160'])
    args = parser.parse_args(sys.argv[1:])

    vkmark = Vkmark(args.iterations, args.resolution)
    vkmark.bench()
    min_score = vkmark.get_min_score()
    max_score = vkmark.get_max_score()
    avg_score = vkmark.get_avg_score()
    print("Vkmark (avg: %s, min: %s, max: %s)" % (str(avg_score), str(min_score), str(max_score)))
