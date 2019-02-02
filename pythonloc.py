#!/usr/bin/env python

import signal
import subprocess
import sys


def null_handler(signum, frame):
    pass


def pythonloc():
    signal.signal(signal.SIGINT, null_handler)
    cmd = [sys.executable] + sys.argv[1:]
    return subprocess.Popen(cmd, env={"PYTHONPATH": "__pypackages__"}).wait()


def piploc():
    signal.signal(signal.SIGINT, null_handler)
    cmd = (
        [sys.executable, "-m", "pip"]
        + sys.argv[1:]
        + ["--system", "--target", "__pypackages__"]
    )
    return subprocess.Popen(cmd, env={"PYTHONPATH": "__pypackages__"}).wait()
