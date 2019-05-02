#!/bin/bash

./brigade.py --iterations=3 --resolution=1920x1080 --preset=Medium
./brigade.py --iterations=3 --resolution=1920x1080 --preset=High
./brigade.py --iterations=3 --resolution=1920x1080 --preset=Ultra

./brigade.py --iterations=3 --resolution=3840x2160 --preset=Medium
./brigade.py --iterations=3 --resolution=3840x2160 --preset=High
./brigade.py --iterations=3 --resolution=3840x2160 --preset=Ultra
