# **pythonloc**: Drop-in Python replacement that imports packages from local directory

<p align="center">
<img src="https://github.com/cs01/pythonloc/raw/master/pythonloc.png"/>
</p>

<a href="https://pypi.python.org/pypi/pythonloc/">
<img src="https://img.shields.io/badge/pypi-0.1.1.1-blue.svg" /></a>

**pythonloc** is a drop in replacement for `python` and `pip` that automatically recognizes a `__pypackages__` directory and prefers importing packages installed in this location over user or global site-packages. If you are familiar with node, `__pypackages__` works similarly to `node_modules`.

So instead of running `python` you run `pythonloc` and the `__pypackages__` path will automatically be searched first for packages. And instead of running `pip` you run `piploc` and it will install/uninstall from `__pypackages__`.

This is an alternative to using Virtual Environments.

This is a Python implementation of [PEP 582](https://www.python.org/dev/peps/pep-0582/), "Python local packages directory". The goal of pythonloc is to make an accessible tool while discussion takes place around adding this functionality to CPython itself. If you prefer, you can [build your own CPython](https://github.com/kushaldas/cpython/tree/pypackages) with these changes instead of using `pythonloc`.

## Testimonials

> Chad has been working and writing some exciting python tools and articles in the packaging/pip space.

— [Jeff Triplett](https://twitter.com/webology/status/1092856644512505856), Python Software Foundation Director

> I’m very enthusiastic about how `__pypackages__` could help simplify and streamline the Python dependencies workflow. Well done on bringing an early prototype implementation for people to test!

— Florimond Manca, Creator of [Bocadillo Project](https://github.com/bocadilloproject)

## System Requirements
* Python 2.7+
* pip


## Installation: What's in the box?
After installing with
```
pip install --user pythonloc
```
or
```
python3 -m pip install --user pythonloc
```
you will have three CLI tools available to you: **pythonloc**, **piploc**, and **pipfreezeloc**.

### pythonloc
Short for "python local", it is a drop-in replacement for python with one important difference: the local directory `__pypackages__/<version>/lib` is added to the front of `sys.path`. `<version>` is the Python version, something like `3.7`. All arguments are forwarded to `python`.

So instead of running
```
python ...
```

you would run

```
pythonloc ...
```

### piploc
Short for "pip local", it invokes pip with the same `sys.path` as `pythonloc`. If installing a package, the target installation directory is modified to be `__pypackages__` instead of the global `site-packages`.

If `__pypackages__` directory does not exist it will be created.

All arguments are forwarded to `pip`.

So instead of running
```
pip ...
```

you would run

```
piploc ...
```

### pipfreezeloc
Running `pip freeze` presents a problem because it shows all installed python packages: those in `site-packages` as well as in `__pypackages__`. You likely only want to output the packages installed to `__pypackages__` and that is exactly what `pipfreezeloc` does.

It is the equivalent of `pip freeze` but only outputs packages in `__pypackages__`. This is required because there is no built-in way to do this with standard pip. For example, the command `pip freeze --target __pypackages__` does not exist.

No arguments are handled with `pipfreezeloc`.

So instead of running
```
pip freeze > requirements.txt
```

you would run

```
pipfreezeloc > requirements.txt
```

## Installing from Lockfiles
This works just like it does in pip. You just need a `requirements.txt` file to install from.

### Installing from `requirements.txt`
```
piploc install -r requirements.txt
pythonloc <app>
```

### Installing from `poetry.lock`
pip cannot read poetry.lock files, so you'll have to generate a requirements.txt file.
```
poetry run pip freeze > requirements.txt
piploc install -r requirements.txt
pythonloc <app>
```

There may be an `export` command coming to `poetry` but it hasn't landed yet. See https://github.com/sdispater/poetry/pull/675.

### Installing from `Pipfile.lock`
pip cannot read `Pipfile`s yet, only pipenv can. So you will need to generate requirements.txt using pipenv.
```
pipenv lock --requirements
pipenv lock --requirements --dev
piploc install -r requirements.txt
pythonloc <app>
```

## Exporting to Lockfiles
```
pipfreezeloc > requirements.txt
```

## Examples

### Script


```python
# myapp.py
import requests
print(requests)
```

```bash
> piploc install requests
Installing collected packages: urllib3, certifi, chardet, idna, requests
Successfully installed certifi-2018.11.29 chardet-3.0.4 idna-2.8 requests-2.21.0 urllib3-1.24.1

> pipfreezeloc
requests==2.21.0

> pythonloc myapp.py  # works!
<module 'requests' from '/tmp/demo/__pypackages__/3.6/lib/requests/__init__.py'>
```

### CLI

You can run any python command with pythonloc and it will just run python under the hood:
```bash
> pythonloc --help
> pythonloc --version
```

Another example showing how imports work:
```bash
> ls

> pythonloc -c "import requests; print(requests)"
Traceback (most recent call last):
  File "<string>", line 1, in <module>
ModuleNotFoundError: No module named 'requests'

> piploc install requests  # installs to __pypackages__/3.6/lib/requests
Installing collected packages: urllib3, certifi, chardet, idna, requests
Successfully installed certifi-2018.11.29 chardet-3.0.4 idna-2.8 requests-2.21.0 urllib3-1.24.1

> pythonloc -c "import requests; print(requests)"  # requests is now found
<module 'requests' from '/tmp/demo/__pypackages__/3.6/lib/requests/__init__.py'>

> piploc uninstall requests  # uninstalls from __pypackages__/3.6/lib/requests
Successfully uninstalled requests-2.21.0
```


## FAQ

### How is this different from a virtual environment?
* A virtual environment may or may not include system packages, whereas `pythonloc` will first look for packages in `.`, then `__pypackages__`, then in other locations such as user or site-packages.
* `pythonloc` does not require activation or deactivation
* `pythonloc` only looks for a local directory called `__pypackages__`. On the other hand, virtual environment activation modifies your `PATH` so you can access virtual environment packages no matter which directory you're in.

### How does it work?
It's quite simple and clocks in at less than lines of 100 code. It uses features already built into Python and pip.

All it does is provide a slight level of indirection when invoking Python and pip. It modifies the `PYTHONPATH` environment variable when running Python to include `__pypackages__`.

If you consult the output of `python --help`, you'll see this:
> PYTHONPATH is a ':'-separated list of directories prefixed to the default module search path.  The result is sys.path.

pythonloc is an alias for `PYTHONPATH=.:__pypackages__/<version>/lib:$PYTHONPATH python PYTHONARGS`

To install packages to the `__pypackages__` directory, it uses pip and runs

```bash
PYTHONPATH=.:__pypackages__/<version>/lib:$PYTHONPATH python -m pip PIPARGS
```
where `PIPARGS` are whatever arguments you pass it, such as `piploc install requests`.

It will insert the arguments `--target __pypackages__` if you are installing a package.

### What actually gets put in `__pypackages__`?
The installed packages go there. This includes their source code, for example the `requests` directory below. metadata about the package is stored in the `*.dist-info` directories.

If you want to modify or debug the source of an installed package, it's very easy to do so. Just open the appropriate file in `__pypackages__` and edit away!
```bash
> piploc install requests
Installing collected packages: urllib3, certifi, chardet, idna, requests
Successfully installed certifi-2018.11.29 chardet-3.0.4 idna-2.8 requests-2.21.0 urllib3-1.24.1


> ls  # note __pypackages__ was created
__pypackages__

> ls __pypackages__/3.6/lib
bin                           idna-2.8.dist-info
certifi                       requests
certifi-2018.11.29.dist-info  requests-2.21.0.dist-info
chardet                       urllib3
chardet-3.0.4.dist-info       urllib3-1.24.1.dist-info
idna
```
### How do I uninstall packages from `__pypackages__`?
`piploc` will automatically add `__pypackages__` to `$PYTHONPATH`, so

```
piploc uninstall PACKAGE
```

will work.

If you get the error

> Not uninstalling PACKAGE at ..., outside environment ...

then run `deactivate` to make sure you are not using a virtual environment, then try again.

### Can I make `python` do this instead of calling `pythonloc`?
An easy way to get this behavior is to create a symlink in your local directory
```
ln -s `which pythonloc` python
ln -s `which piploc` pip
```
Then run them with
```
./python
./pip
```
Otherwise you'll have to build CPython yourself with the [reference implementation](https://github.com/kushaldas/cpython/tree/pypackages) on GitHub.

### Why not use the reference implementation of PEP 582?
There is more overhead involved in building and distributing a custom CPython build than installing a pip package.

You are encouraged to check it out if you are interested though, it's pretty cool!

If it gets accepted and added to CPython then `pythonloc` may not be needed anymore.

* [PEP 582](https://www.python.org/dev/peps/pep-0582/)
* [reference CPython implementation](https://github.com/kushaldas/cpython/tree/pypackages) on GitHub
