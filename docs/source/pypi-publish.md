Publishing to PyPi
==================

Publishing your python package to PyPi will mean that other people can install it using e.g.

```
pip install projectName
```

And then import the package into their python projects using

```
import projectName
```

A tutorial for how to do this can be found here:
[https://packaging.python.org/en/latest/tutorials/packaging-projects/](https://packaging.python.org/en/latest/tutorials/packaging-projects/)

Some notes *relative* to the tutorial are included here.

## Creating the package files

If you're using this template, you already have a `pyproject.toml`, `LICENSE` and `README.md` file in the root directory of your repository.  You also have the `tests/` directory and your package files are in `template_project/` rather than `src/`.

The file `pyproject.toml`  configures the metadata for your project.

### Choosing a build backend

The default example in the tutorial specifies "Hatchling" to convert your package to a distribution package.

```
[build-system]
requires = ["hatchling >= 1.26"]
build-backend = "hatchling.build"
```

In template-project, we instead have
```
[build-system]
build-backend = "setuptools.build_meta"
requires = [
  "setuptools>=42",
  "setuptools-scm[toml]>=3.4",
  "wheel",
]
```

### Configuring metadata

As of April 2025, the example from the tutorial shows:
```
[project]
name = "example_package_YOUR_USERNAME_HERE"
version = "0.0.1"
authors = [
  { name="Example Author", email="author@example.com" },
]
description = "A small example package"
readme = "README.md"
requires-python = ">=3.8"
classifiers = [
    "Programming Language :: Python :: 3",
    "Operating System :: OS Independent",
]
license = "MIT"
license-files = ["LICEN[CS]E*"]

[project.urls]
Homepage = "https://github.com/pypa/sampleproject"
Issues = "https://github.com/pypa/sampleproject/issues"
```

where in this template, we have
```
[project]
name = "template-project-efw"
description = "Example template project for docs, pip install and git"
readme = "README.md"
license = { file = "LICENSE" }
maintainers = [
  { name = "Eleanor Frajka-Williams", email = "eleanorfrajka@gmail.com" },
]
requires-python = ">=3.8"
classifiers = [
  "Programming Language :: Python :: 3 :: Only",
  "Programming Language :: Python :: 3.8",
  "Programming Language :: Python :: 3.9",
  "Programming Language :: Python :: 3.10",
  "Programming Language :: Python :: 3.11",
  "Programming Language :: Python :: 3.12",
]
dynamic = [
  "dependencies",
  "version",
]
urls.documentation = "https://github.com/eleanorfrajka/template-project"
urls.homepage = "https://github.com/eleanorfrajka/template-project"
urls.repository = "https://github.com/eleanorfrajka/template-project"
```

In our case, the "name" (used for the name of the project on PyPi) is "template-project-efw" to make it a unique package, whereas the repository name is "template-project" on github.

Our version also tries to dynamically assign the version number, which will come out of `template_project/_version.py`.

In `pyproject.toml` we have:
```
[tool.setuptools_scm]
write_to = "template_project/_version.py"
write_to_template = "__version__ = '{version}'"
tag_regex = "^(?P<prefix>v)?(?P<version>[^\\+]+)(?P<suffix>.*)?$"
local_scheme = "no-local-version"
```

*Action:** You should change the name, description, maintainers and urls to match your repository.

### Generating distribution archives

Run the next steps to generate the distribution.

First, make sure you have the latest version of `build` installed:
```
python3 -m pip install --upgrade build
```

Then run this from the directory where `pyproject.toml` is located:
```
python3 -m build
```

## Uploading the distribution archives

### First time: Test it on testpypi first
1. Create an account on [https://test.pypi.org/account/register](https://test.pypi.org/account/register).  You'll need a 2FA app, e.g. on your phone.  If you already have an account, then you can login to your account at [https://test.pypi.org/](https://test.pypi.org), but this isn't necessary to run the test.

2. To upload your project, you'll need an API token.  Save this somewhere on your computer (not in your git repository).

3. Install twine (see tutorial instructions) or upgrade:
```
python3 -m pip install --upgrade twine
```

4. Run twine to upload the archives in `dist/`

```
python3 -m twine upload --repository testpypi dist/*
```

If you get an error like
```
ERROR    InvalidDistribution: Invalid distribution metadata: unrecognized or malformed field 'license-file'
```
this is due to using the newest `twine` with oldish `packaging` and a build backend that produces invalid metadata.  Upgrade your packaging: `pip install -U packaging .`, and try again.

5. Verify that it works to install your package.  Create a virtual environment and install from testpypi as (CHANGING the package name to whatever yours is called)

```
pip install -i https://test.pypi.org/simple/ --no-deps template-project-efw
```

### Going live on pypi

Repeat the steps above but on [https://pypi.org](https://pypi.org).  You'll need a separate API token (save this on your computer!) and the final upload step will be

```
python3 -m twine upload dist/*
```

### Allowing Github releases to update the project on PyPi

To automatically generate the new release on PyPi using Github actions, you need (1) the workflow (see `.github/workflows/pypi.yml` in this template) and (2) to setup (on https://pypi.org) GitHub as a "trusted publisher".

See [https://github.com/marketplace/actions/pypi-publish#trusted-publishing](https://github.com/marketplace/actions/pypi-publish#trusted-publishing) or [https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/](https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/) for more information.
