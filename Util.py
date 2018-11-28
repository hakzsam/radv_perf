#!/bin/python

def get_file_contents(filename):
    with open(filename, 'r') as f:
        return f.read()
    return None
