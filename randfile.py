#!/usr/bin/env python
"""
    Generates a file with random content in a reproducible way.

SYNOPSIS
    randfile [-h][-s size][-v version]

OPTIONS
    -h  This help page
    -v  version
            Requests a specific version of python different than the default.
            This option can be used to ensure that the output is reproducible on
            systems where the default version of python is not available
    -s size
            Number of bytes to produce. Standard suffices 'KB', 'MB', 'GB',
            or 'TB' for standard units and 'KiB', 'MiB', 'GiB', or 'TiB' for
            binary units are supported. Eg. '100MiB' mean 100 Mebibytes. Note
            that when using a suffix, the buffering of output is adjusted
            accordingly (eg. -s 1000000 is much slower than -s 1MB).

COMPLIANCE
    This program should work with python version > 2.6 (including 3.x)

"""

from __future__ import print_function
import random,getopt,sys,os,io

step = 1

DEFAULT_FILESIZE="1GiB"  # Override with option -s
DEFAULT_PYTHON_VERSION="3.5.2" # override with option -v


IBISIZES = {'T': 1024**4, 'G': 1024**3, 'M': 1024**2, 'K': 1024}
DECSIZES = {'T': 1000**4, 'G': 1000**3, 'M': 1000**2, 'K': 1000}

def parse_bytes(size_str,tab_sizes):
    global step
    mult = tab_sizes[size_str[-1]]
    if size_str[-1] != 'K':
        step = tab_sizes['M']
    else:
        step = tab_sizes['K']
    return int(size_str[:-1]) * mult

def parse_size(size):
    if size[-1] == 'B':
        if size[-2] == 'i':
            return parse_bytes(size[:-2],IBISIZES)
        else:
            return parse_bytes(size[:-1],DECSIZES)
    else:
        return int(size)

def usage(name):
    help(name)

def parse_args(argv):
    (options,args) = getopt.getopt(argv,"s:v:h")

    requested_version = DEFAULT_PYTHON_VERSION
    requested_size = DEFAULT_FILESIZE

    for opt in options:
        if opt[0] == "-h":
            usage(__name__)
            sys.exit(0)
        if opt[0] == "-v":
            requested_version = opt[1]
            continue
        if opt[0] == "-s":
            requested_size = opt[1]
            continue

    version = "%s.%s.%s"%sys.version_info[:3]

    try:
        assert version == requested_version
    except AssertionError as ae:
        print("Wrong version of python. Expected=%s, current=%s"
            %(requested_version,version), file=sys.stderr)
        sys.exit(1)

    size = parse_size(requested_size)
    print("size=%s (%f MiB, %f MB)"%(size, float(size)/float(1024**2),
        float(size)/float(1000**2)), file=sys.stderr)
    return size

if __name__ == "__main__":
    size = parse_args(sys.argv[1:])
    random.seed(0)
    #sys.stdout = sys.stdout.buffer
    raw_output = io.open(1,"ab")
    #step=10
    for s in range(int(size/step)):
        val = [ random.randint(0,255) for i in range(step) ]
        # Writing bytes on output is tricky in Python
        # No single way between 2.x and 3.x
        if sys.version_info[0] >= 3:
            os.write(1,bytes(val))
        else:
            string = ""
            for x in val:
                string = string + chr(x)
            raw_output.write(string)
        size = size - 1
    #sys.stdout = sys.__stdout__
