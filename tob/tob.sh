#!/bin/bash

# Estimated time: 30 min

./tob.py --iterations=3 --resolution=1920x1080 --preset=low
./tob.py --iterations=3 --resolution=1920x1080 --preset=medium
./tob.py --iterations=3 --resolution=1920x1080 --preset=high
./tob.py --iterations=3 --resolution=1920x1080 --preset=ultra
./tob.py --iterations=3 --resolution=1920x1080 --preset=extreme

./tob.py --iterations=3 --resolution=2560x1440 --preset=low
./tob.py --iterations=3 --resolution=2560x1440 --preset=medium
./tob.py --iterations=3 --resolution=2560x1440 --preset=high
./tob.py --iterations=3 --resolution=2560x1440 --preset=ultra
./tob.py --iterations=3 --resolution=2560x1440 --preset=extreme

./tob.py --iterations=3 --resolution=3840x2160 --preset=low
./tob.py --iterations=3 --resolution=3840x2160 --preset=medium
./tob.py --iterations=3 --resolution=3840x2160 --preset=high
./tob.py --iterations=3 --resolution=3840x2160 --preset=ultra
./tob.py --iterations=3 --resolution=3840x2160 --preset=extreme
