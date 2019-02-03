#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import signal
import subprocess
import sys
import pip


def get_target_dir():
    """returns path in compliance with PEP 582
    https://www.python.org/dev/peps/pep-0582/
    """
    return os.path.join(
        "__pypackages__",
        str(sys.version_info.major) + "." + str(sys.version_info.minor),
        "lib",
    )


def get_env():
    env = dict(os.environ)
    env["PYTHONPATH"] = ".:" + get_target_dir() + ":" + env.get("PYTHONPATH", "")
    return env


def null_handler(signum, frame):
    pass


def pythonloc():
    signal.signal(signal.SIGINT, null_handler)
    cmd = [sys.executable] + sys.argv[1:]
    return subprocess.Popen(cmd, env=get_env()).wait()


def _get_pip_target_args(pip_args):
    if "install" in pip_args:
        if "--target" not in pip_args:
            # use target dir if installing
            target = ["--target", get_target_dir()]
        if (
            pip.__version__.startswith("9.") or pip.__version__.startswith("10.")
        ) and "--system" not in pip_args:
            target += ["--system"]
    else:
        target = []
    return target


def piploc():
    signal.signal(signal.SIGINT, null_handler)
    pip_args = sys.argv[1:]
    target = _get_pip_target_args(pip_args)
    cmd = [sys.executable, "-m", "pip"] + pip_args + target
    return subprocess.Popen(cmd, env=get_env()).wait()


def pipfreezeloc():
    cmd = [sys.executable, "-m", "pip", "freeze"]
    p = subprocess.Popen(cmd, env=get_env(), stdout=subprocess.PIPE)
    try:
        outs, errs = p.communicate()
        if outs is None:
            all_reqs = set()
        else:
            all_reqs = set(outs.decode().split("\n"))
    except Exception:
        p.kill()
        exit("failed to run pip freeze")

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    try:
        outs, errs = p.communicate()
        if outs is None:
            sys_reqs = set()
        else:
            sys_reqs = set(outs.decode().split("\n"))
    except Exception:
        p.kill()
        exit("failed to run pip freeze")
    for i in all_reqs - sys_reqs:
        print(i)
