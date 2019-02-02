#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import signal
import subprocess
import sys
import pip


def get_env():
    env = dict(os.environ)
    env["PYTHONPATH"] = "__pypackages__:" + env.get("PYTHONPATH", ":")
    return env


def null_handler(signum, frame):
    pass


def pythonloc():
    signal.signal(signal.SIGINT, null_handler)
    cmd = [sys.executable] + sys.argv[1:]
    return subprocess.Popen(cmd, env=get_env()).wait()


def piploc():
    signal.signal(signal.SIGINT, null_handler)
    pip_args = sys.argv[1:]

    if "install" in pip_args:
        if "--target" not in pip_args:
            # use target dir if installing
            target = ["--target", "__pypackages__"]
        if (
            pip.__version__.startswith("9.") or pip.__version__.startswith("10.")
        ) and "--system" not in pip_args:
            target += ["--system"]
    else:
        target = []

    cmd = [sys.executable, "-m", "pip"] + pip_args + target
    return subprocess.Popen(cmd, env=get_env()).wait()
