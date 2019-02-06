#!/bin/python

import json
import sys

from termcolor import colored

def get_data_from_file(filename):
    data = []
    with open(filename) as f:
        for line in f:
            json_acceptable_string = line.replace("'", "\"")
            d = json.loads(json_acceptable_string)
            data.append(d)
    return data

def equal_dicts(d1, d2, ignore_keys=()):
    d1_, d2_ = d1.copy(), d2.copy()
    for k in ignore_keys:
        try:
            del d1_[k]
        except KeyError:
            pass
        try:
            del d2_[k]
        except KeyError:
            pass

    return d1_ == d2_

def compute_diff(a, b):
    a_ = float(a)
    b_ = float(b)
    return round((b_ - a_) / a_ * 100.0, 2)

if __name__ == "__main__":
    old = sys.argv[1]
    new = sys.argv[2]

    # Read and convert string to dictionary.
    old_data = get_data_from_file(old)
    new_data = get_data_from_file(new)

    # List of keys to ignore for comparing old and new results.
    ignored_keys = ["iterations",
                    "avg_score",
                    "min_score",
                    "max_score",
                    "avg_fps",
                    "min_fps",
                    "max_fps"]

    results = []
    for old_dict in old_data:
        for new_dict in new_data:
            if equal_dicts(old_dict, new_dict, ignored_keys):
                result = old_dict.copy()

                # Delete all ignored keys from the result entry.
                for k in ignored_keys:
                    if k in result:
                        del result[k]

                if "avg_fps" in old_dict:
                    result["old_avg_fps"] = old_dict["avg_fps"]
                    result["new_avg_fps"] = new_dict["avg_fps"]
                    result["diff"] = str(compute_diff(result["old_avg_fps"], result["new_avg_fps"]))
                elif "avg_score" in old_dict:
                    result["old_avg_score"] = old_dict["avg_score"]
                    result["new_avg_score"] = new_dict["avg_score"]
                    result["diff"] = str(compute_diff(result["old_avg_score"], result["new_avg_score"]))
                results.append(result)

    print("HURT:")
    for r in results:
        if float(r["diff"]) < 0.0:
            print(colored(r, 'red'))

    print("GAIN:")
    for r in results:
        if float(r["diff"]) >= 0.0:
            print(colored(r, 'green'))
