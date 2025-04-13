Extra GitHub features: Actions & Pages
======================================

Much of the explanation in [Collaborate with git](gitcollab) can be done whether your repository lives on GitHub or a GitLab server or elsewhere.  In this template-project, we use GitHub-specific features to perform extra functions that may not look the same on other git servers.

On GitHub, we are using two main features:

    - GitHub Actions (via workflows)
    - GitHub Pages: to display the documentation as a website (here as https://eleanorfrajka.github.io/template-project)

GitHub Actions provide a way to

    - automatically run code tests (tests which you have written, normally stored in the `tests/` directory) when you make a pull request.  This can help ensure that a change to the code in one place doesn't break the code elsewhere.

    - automatically build documentation using the latest changes in code.  If you add a function or change its "docstring" (the comment at the top of the function), the html documentation can be automatically updated without you editing it.

The steps of the action are stored as yaml files (`*.yml`) within the repository in the directory `.github/workflows`.  Check, e.g. in this repository, the [tests.yml](https://github.com/eleanorfrajka/template-project/blob/main/.github/workflows/tests.yml) file.

#### GitHub Action to run test code

##### Structure of a workflow yaml file
Note that in the yaml file for GitHub Actions, the indentation matters, and there are expected commands to be parsed.  Here, we start with

```
name: Run tests
```
This specifies the name which will appear in the left hand sidebar on the github repository when you click "Actions" across the top (or navigate directly to the example in this template-project here: https://github.com/eleanorfrajka/template-project/actions).  Generally, the text to the right of the colon space for a name ("name: ") can be free text, but avoid fancy punctuation which may cause problems.

Note under "All workflows", a workflow named "Run tests"

The next lines specify when the action should be "triggered".  I.e., what git activity in this repository will cause the workflow to run.

```
on:
  pull_request:
    branches:
      - main
    paths:
      - '**.py'
      - '**.ipynb'
```
Here, we've specified that when a "pull request" is created, that the tests should be run.  This occurs after step 8 "Compare pull request on Github.com" in [Collaborate with git](gitcollab).  It will only trigger when the pull request is made on the "main" branch (note that "main" used to be called "master") and searches through for files matching the name `**.py` or `**.ipynb` (i.e., python files or notebooks).

The next part of the workflow lists the various jobs to be run.  We use
```
jobs:
  job_mytests:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ["3.8", "3.12"]
      fail-fast: true
    defaults:
      run:
        shell: bash -l {0}
```
where the text "job_mytests" is somewhat arbitrary, but the lines following tell the test to run through a set of different operating systems (e.g., run the test as if it were on linux, windows or mac) and the options for python versions include a couple (so the tests can check whether a specific python version causes a problem).  The `fail-fast: true` option says that if any one test fails, stop running the rest of the tests.

Finally, the actual steps to be evaluated come after `steps:` as
```
    steps:
    - name: Run a one-line script
      run: echo "The job was automatically triggered by a ${{ github.event_name }} event."
    - uses: actions/checkout@v4

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v2
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        python -m pip install flake8 pytest
        if [ -f requirements-dev.txt ]; then pip install -r requirements-dev.txt; fi
    - name: Test with pytest
      run: |
        pytest
```

We've included a very simple one to print what kind of event triggered the test.

Then we checkout the repository using an action provided on GitHub [actions/checkout@v4](https://github.com/marketplace/actions/checkout).  Note that you may need to update to later versions.

Then we set up the version of python to be used, cycling through the options given in `matrix.python-version` using [actions/checkout@v2](https://github.com/marketplace/actions/setup-python).

The "Install dependencies" step reads from the `requirements-dev.txt` file, which specifies which python packages are needed for development work.  `requirements-dev.txt` should include all packages listed in `requirements.txt` but additional packages needed to run these tests or build the documentation.  For example, running these tests requires the package `pytest` which is used in the step "Test with pytest".

##### Viewing the executed Action on GitHub

To see an example of the executed action, go to [https://github.com/eleanorfrajka/template-project/actions/runs/12084492287](https://github.com/eleanorfrajka/template-project/actions/runs/12084492287), which ran the tests for this repository.

On the left, you'll see green ticks next to the tests which ran successfully.  You can also see where it cycled through each combination of operating system and python version.  E.g., the first run used "ubuntu-latest" as the operating system and "3.8" as the python version.

If you select one on the left, you can then see the steps that were carried out on the right.  Clicking a step, you can see some details about the run and any output generated.

For an example of a failed test, see [https://github.com/eleanorfrajka/template-project/actions/runs/12084406484/job/33699533161](https://github.com/eleanorfrajka/template-project/actions/runs/12084406484/job/33699533161).  Click one of the tests with a red x, and the steps will appear to the right.  Click the step where there was an error (red x) and the error message appears.

In this case, the test was unable to run because there was some legacy code that wasn't applicable here (and also not available), where the `tests/test_tools.py` tried to import a package that didn't exist (`seagliderOG1`).  The error message reads as
```
==================================== ERRORS ====================================
_____________________ ERROR collecting tests/test_tools.py _____________________
ImportError while importing test module '/Users/runner/work/template-project/template-project/tests/test_tools.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_tools.py:8: in <module>
    from seagliderOG1 import tools
E   ModuleNotFoundError: No module named 'seagliderOG1'
=========================== short test summary info ============================
ERROR tests/test_tools.py
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
=============================== 1 error in 0.10s ===============================
Error: Process completed with exit code 2.
```

These error messages are helpful for understanding why the action failed.

Additionally or alternatively, you can try to run the steps in order on your computer (without specifying the operating system or python version), by parsing through the commands specified in the steps of the yaml file.

##### Failed tests in a pull request

If your pull request fails a test, **do not merge**.  By working in the same branch, you can try other fixes until the test successfully runs (or you can ask for a review on GitHub by naming a collaborator in the "Assignee" to the right on a pull request).

See pull request (PR) [#1](https://github.com/eleanorfrajka/template-project/pull/1).  Scrolling down, you can see each commit that was tried, and whether or not the tests ran (red x = failed, green check = success).  In this case, after the tests passed, the pull request was merged which closes the pull request.

#### GitHub Action to build documentation

##### Creating docs with sphinx

In this template, we are creating documentation using `sphinx` with a "read the docs" theme.  This requires extra packages in your `requirements-dev.txt` file:
```
sphinx
sphinx-rtd-theme
pypandoc
nbsphinx
nbconvert
myst-nb
```
The `sphinx` is the basic machinery, and `sphinx-rtd-theme` is the "read the docs" theme.  `pypandoc` is a pandoc translater which enables translation from markdown, rst, python etc into formats like html, latex, etc.

The additional `nbsphinx` and `nbconvert` are to handle python notebooks, so that they can be displayed in the sphinx output.  `myst_parser` allows you to include documentation files as `.md` in addition to sphinx's default, `.rst`.

The extra structure within the repository, within the `docs/` directory includes a `Makefile` and `source/conf.py` with some configuration information.  **You should edit `conf.py` to match your repository,** especially the "general information about this project" section.

When you'd like to test the build of your documentation (prior to submitting pull requests to the repository), navigate to the `docs/` directory in a terminal window, and run
```
template-project/docs $ make html
```
This will generate the website within the directory `docs/build/html/`, which you can open from a browser to verify that everything worked.

##### Workflows to build documentation

In the template-project, we have two workflows for building documentation.

To test that the documentation can build, there is `.github/workflows/docs.yml` (named "Test documentation build" and viewable on GitHub Actions here: https://github.com/eleanorfrajka/template-project/actions/workflows/docs.yml)

To deploy the documentation to the branch `gh-pages` *after* a successful pull request is merged, there is `.github/workflows/deploy_docs.yml` (named "Deploy Documentation" and viewable here: https://github.com/eleanorfrajka/template-project/actions/workflows/docs_deploy.yml)

Both of these use the same set of steps as `.github/workflows/tests.yml` but with a couple notable differences.

In `docs.yml`, we are not bothering with testing on a range of operating systems and so specify only `runs-on: ubuntu-latest`.  This could be any operating system, but on GitHub, windows appears to be slower.

We're also using a different way to set up python and the environment for execution.  In `tests.yml` this was done via the `actions/setup-python@v2` and pip to install based on `requirements-dev.txt`.
```
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v2
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        python -m pip install flake8 pytest
        if [ -f requirements-dev.txt ]; then pip install -r requirements-dev.txt; fi
```
In `docs.yml`, we are instead using micromamba to manage the environment.
```
    - name: Setup Micromamba ${{ matrix.python-version }}
      uses: mamba-org/setup-micromamba@v2.0.1
      with:
        environment-name: TEST
        init-shell: bash
        create-args: >-
          python=3 pip
          --file requirements-dev.txt
          --channel conda-forge
```
This is due to some errors encountered when GitHub Actions ran `docs.yml` workflow associated with the installation of `pandoc` (required for `sphinx` which is what we're using to build the documentation).  See some detail about the errors here: https://github.com/eleanorfrajka/template-project/pull/3.  So, while `tests.yml` would work with either method, we are switching to the micromamba method for `docs.yml` and `docs_deploy.yml`.

##### Getting docs as a GitHub Pages

Once the `docs_deploy.yml` has successfully run (after merging a "pull request" onto main, which triggers the conditions "push on main") at the top of `docs_deploy.yml`:
```
on:
  # This will run on commits with a pull request
  push:
    branches:
      - main
```

The last step "Deploy" generates or updates the `gh-pages` branch: https://github.com/eleanorfrajka/template-project/tree/gh-pages
```
    - name: Deploy
      uses: peaceiris/actions-gh-pages@v4
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: docs/build/html
```
This uses the GitHub Action `peaceiris/actions-gh-pages@v4` (https://github.com/marketplace/actions/github-pages-action).

##### Activating `github.io/template-project'

You'll know you're ready for this step when, from the main Github website for the repository (e.g. https;//github.com/eleanorfrajka/template-project/) if you click the drop-down button in the upper left quadrant that says "main", you can scroll through and find the branch "gh-pages".

Now you're ready to set up "Github Pages".

1. Navigate to the repository and click the "Settings" across the top bar (to the right of "Insights"), then in the left sidebar, choose "Pages".

2. Select the "Source" as "Deploy from a branch" and in the next line, "Branch", choose in the dropdown not "main" but "gh-pages".  Leave the rest of the settings and click "save".  This tells GitHub to serve the root level of this branch as the pages.

**Note:** If you're following the steps in this template, you should not edit within your `gh-pages` branch since all of the contents here will be automatically generated from the `docs_deploy.yml` using your `notebooks/demo.ipynb` notebook and contents in the repository found in the `docs/` directory.

3. Then, to help others find your pages, go back to your repository and click the settings cogwheel in the right side bar next to the "About" header.  For the "Website", tick the box that says "Use your GitHub Pages website".  This will auto-populate the URL into the Website box.  Click "save changes".
