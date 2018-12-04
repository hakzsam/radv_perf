#!/bin/bash

# Estimated time: 17min

# 4k
./tw2.py --iterations=3 --resolution=3840x2160 --preset=ultra --scene=fallen
./tw2.py --iterations=3 --resolution=3840x2160 --preset=ultra --scene=skaven
./tw2.py --iterations=3 --resolution=3840x2160 --preset=high --scene=fallen
./tw2.py --iterations=3 --resolution=3840x2160 --preset=high --scene=skaven

# 1080p
./tw2.py --iterations=3 --resolution=1920x1080 --preset=ultra --scene=fallen
./tw2.py --iterations=3 --resolution=1920x1080 --preset=ultra --scene=skaven
./tw2.py --iterations=3 --resolution=1920x1080 --preset=high --scene=fallen
./tw2.py --iterations=3 --resolution=1920x1080 --preset=high --scene=skaven
