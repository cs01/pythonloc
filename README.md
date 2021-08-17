# **pythonloc**: Drop-in Python replacement that imports packages from local directory

<p align="center">
<img src="https://github.com/cs01/pythonloc/raw/master/pythonloc.png"/>
</p>

<a href="https://badge.fury.io/py/pythonloc"><img src="https://badge.fury.io/py/pythonloc.svg" alt="PyPI version" height="18"></a>

**pythonloc** is a drop in replacement for `python` and `pip` that automatically recognizes a `__pypackages__` directory and prefers importing packages installed in this location over user or global site-packages. If you are familiar with node, `__pypackages__` works similarly to `node_modules`.

So instead of running `python` you run `pythonloc` and the `__pypackages__` path will automatically be searched first for packages. And instead of running `pip` you run `piploc` and it will install/uninstall from `__pypackages__`.

This is an alternative to using Virtual Environments.

This is a Python implementation of [PEP 582](https://www.python.org/dev/peps/pep-0582/), "Python local packages directory". The goal of pythonloc is to make an accessible tool while discussion takes place around adding this functionality to CPython itself. If you prefer, you can [build your own CPython](https://github.com/kushaldas/cpython/tree/pypackages) with these changes instead of using `pythonloc`.

**Please note that PEP 582 has not been accepted. It may or not be accepted in the long term. `pythonloc` is experimental and its API may change in the future.**

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

## Testimonials

*Featured on [episode #117](https://pythonbytes.fm/episodes/show/117/is-this-the-end-of-python-virtual-environments) of the Python bytes podcast.*

"Chad has been working and writing some exciting python tools and articles in the packaging/pip space."

— [Jeff Triplett](https://twitter.com/webology/status/1092856644512505856), Python Software Foundation Director

"I’m very enthusiastic about how `__pypackages__` could help simplify and streamline the Python dependencies workflow. Well done on bringing an early prototype implementation for people to test!"

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
you will have four CLI tools available to you: **pythonloc**, **piploc**, **pipx**, and **pipfreezeloc**.

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

If PEP 582 is adopted, `python` itself will have this behavior.

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

If PEP 582 is adopted, I think `pip` should default to working in the appropriate `__pypackages__` directory. A flag can be added to install to site-packages, if desired.

### pipx
*Note: pipx is included with pythonloc for Python 3.6+ only.*

Installing packages that have so called "entry points" to `__pypackages__` presents a problem. The entry points, or "binaries", are no longer available on your $PATH as they would be if you installed in a virtual environment or to your system. These binaries are massively popular and useful. Examples of binaries are `black`, `pytest`, `tox`, `flake8`, `mypy`, `poetry`, and `pipenv` (and indeed `pythonloc` itself).

`pipx` is a binary installer and runner for Python that, when run, searches for a binary in the appropriate `__pypackages__` location and runs it. If you are familiar with JavaScript's [`npx`](https://www.npmjs.com/package/npx), it's similar to that.

So instead of running
```
BINARY [BINARY ARGS]
```
you would run
```
pipx run BINARY [BINARY ARGS]
```
If not found, pipx will install and run it from a temporary directory. If you require the binary to be found in the `__pypackages__` directory, you can run
```
pipx run --pypackages BINARY [BINARY ARGS]
```
If the binary is not found, and error will be presented.

**Note**: When installing a new package to an existing `__pypackages__` directory, the entry points will not be created in `.../3.6/lib/bin`, for example, if something is already there. To do that, you need to run `piploc install -U PACKAGE`. When you do that, the entire contents of the directory will be replaced. Fixing this would require a modification to `pip` itself.

If PEP 582 is adopted, `pipx` will be a good companion tool to run binaries.

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

If PEP 582 is adopted, a more robust solution to freezing the state of `__pypackages__` should be created.

## Installing from requirements.txt/Lockfiles
This works just like it does in pip. You just need a `requirements.txt` file to install from.

### Installing from `requirements.txt`
```
piploc install -r requirements.txt
pythonloc <app>
```

### Installing from `poetry.lock`
pip cannot read poetry.lock files, so you'll have to generate a requirements.txt file.

Poetry 1.x provides `export` command:
```bash
poetry self:update --preview #  install 1.x version of Poetry
poetry export -f requirements.txt
piploc install -r requirements.txt
pythonloc <app>
```

For Poetry 0.x you can adopt the next approach:
```bash
poetry run pip freeze > requirements.txt
piploc install -r requirements.txt
pythonloc <app>
```


### Installing from `Pipfile.lock`
pip cannot read `Pipfile`s yet, only pipenv can. So you will need to generate requirements.txt using pipenv.
```
pipenv lock --requirements
pipenv lock --requirements --dev
piploc install -r requirements.txt
pythonloc <app>
```

In the long term tools will be able to install directly to `__pypackages__` or piploc will be able to read various lockfile formats.


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

## Entry Points / Binaries
```
> piploc install cowsay
Collecting cowsay
  Using cached https://files.pythonhosted.org/packages/e7/e7/e93f311adf63ac8936beb962223771b1ab61227ae3d9ec86e8d9f8f9da1c/cowsay-2.0-py2.py3-none-any.whl
Installing collected packages: cowsay
Successfully installed cowsay-2.0

> pipx run cowsay moooo from local __pypackages__!
  ________________________________
< moooo from local __pypackages__! >
  ================================
                                     \
                                      \
                                        ^__^
                                        (oo)\_______
                                        (__)\       )\/       ||----w |
                                            ||     ||


```

## Downsides?

While this PEP is pretty exciting, there are a some things it doesn't solve.

* OS-dependent packages: The directory structure in `__pypackages__` is namespaced on python version, so packages for Python 3.6 will not mix with 3.7, which is great. But sometimes packages install differently for different OS's, so Windows may not match mac, etc.
* site-packages: This PEP first looks to `__pypackages__` but will fall back to looking in `site-packages`. This is not entirely hermetic and could lead to some confusion around which packages are being used. I would prefer the default search path be **only** `__pypackages__` and nothing else.
* perceived downside -- bloat: Many have brought this up in various forums, comparing it to `node_modules`, but I don't think it applies here. For one, the same if not more content is installed into a virtual environment, so this just moves it into a local directory. No additional bloat. In fact, it is more obvious and can be deleted because it's not hidden away in a virtual env directory.  But more importantly, I think the assumption that it is bloated or will be abused stems from JavaScript's ecosystem. JavaScript has a notoriously limited standard library, and developers need to reach for third party packages more often. In addition, the JavaScript community heavily relies on many plugins and transpilation. Python does not. I do not find the bloat argument convincing.
* Some pip installation idiosyncracies. For example, `pip install` with `--target` will wipe out content in the `lib/bin` directory when the `-U` flag is passed, but not put anything there when it's not passed.

## FAQ

### How is this different from a virtual environment?
* A virtual environment may or may not include system packages, whereas `pythonloc` will first look for packages in `.`, then `__pypackages__`, then in other locations such as user or site-packages.
* `pythonloc` does not require activation or deactivation
* `pythonloc` only looks for a local directory called `__pypackages__`. On the other hand, virtual environment activation modifies your `PATH` so you can access virtual environment packages no matter which directory you're in.

### How does it work?
It's quite simple and clocks in at less than 100 lines of code. It uses features already built into Python and pip.

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
