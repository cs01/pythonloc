#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import sys
import pip


def get_pypackages_lib_path(script_path=None):
    """returns path in compliance with PEP 582
    https://www.python.org/dev/peps/pep-0582/
    """
    if script_path:
        # use __pypackages__ relative to the script being run
        pypackages = os.path.join(os.path.dirname(script_path), "__pypackages__")
    else:
        pypackages = "__pypackages__"

    return os.path.join(
        pypackages,
        str(sys.version_info.major) + "." + str(sys.version_info.minor),
        "lib",
    )


def get_env(script_path=None):
    env = dict(os.environ)
    env["PYTHONPATH"] = (
        ".:" + get_pypackages_lib_path(script_path) + ":" + env.get("PYTHONPATH", "")
    )
    return env


def null_handler(signum, frame):
    pass


def get_script_path():
    for arg in sys.argv[1:]:
        if not arg.startswith("-"):
            return os.path.abspath(arg)
    return None


def pythonloc():
    args = [sys.executable] + sys.argv[1:]
    script_path = get_script_path()
    os.execve(sys.executable, args, get_env(script_path))


def _get_pip_target_args(pip_args):
    if "install" in pip_args:
        if "--target" not in pip_args:
            # use target dir if installing
            target = ["--target", get_pypackages_lib_path()]
        if (
            pip.__version__.startswith("9.") or pip.__version__.startswith("10.")
        ) and "--system" not in pip_args:
            target += ["--system"]
    else:
        target = []
    return target


def piploc():
    pip_args = sys.argv[1:]
    target = _get_pip_target_args(pip_args)
    args = [sys.executable] + ["-m", "pip"] + pip_args + target
    os.execve(sys.executable, args, get_env())


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


if __name__ == "__main__":
    pythonloc()
