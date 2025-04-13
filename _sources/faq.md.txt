FAQ / Troubleshooting
======================


#### I get an error when doing `from template_project import plotters`

This is because your code can't find the project `template_project`.

**Option 1:** Install the package `template_project` locally

Activate your environment.

```
micromamba activate template_env
```

then install your project from the terminal window in, e.g., `/Users/eddifying/github/template-project` as
```
pip install -e .
```
This will set it up so that you are installing the package in "editable" mode.  Then any changes you make to the scripts will be taken into account (though you may need to restart your kernel).

**Option 2:** Add the path to the `template_project` to the code

Alternatively, you could add to your notebook some lines so that your code can "find" the package.  This might look like
```
import sys
sys.path.append('/Users/eddifying/github/template-project')
```
before the line where you try `from template_project import plotters`.  The secon

#### Failing to install the package in a Github Action

```
× Getting requirements to build editable did not run successfully.
│ exit code: 1
╰─> See above for output.
```

To test the installation, you'll want a fresh environment.

**In a terminal window, at the root of your project** (for me, this is `/Users/eddifying/github/template-project/`), run the following commands in order.
```
virtualenv venv
source venv/bin/activate && micromamba deactivate
pip install -r requirements.txt
pip install -e .
```

Then check and troubleshoot any errors.  When this runs, you are probably ready to try it with the GitHub Actions (where the workflows are in your repository in `.github/workflows/*.yml`)

#### What's the difference between `template-project` and `template_project`??

Our repository is called `template-project`.  You can have dashes in a repository name.

Within the repository, the code (`*.py` files) are located in a subdirectory called `template_project`.  This is the package or module that we are creating and that will be installed, e.g., by `pip` when you do a `pip install -e .`.  Python packages should not have dashes in them!

**Could we have called them both `template_project`?**  Yes!

**Could we have called them both `template-project`?**  No!  Not recommended for python packages even though it's totally fine for repositories.

**Why did you do this confusing thing in the template?**  Two answers: First, by accident.  It was called `template-project/projectName` but since it appears to be common practice to have the package/module with the same name as the repository, this would mean `projectName` should be more like `template project`.  But it also provides some clarity for what we're talking about in the various steps--as long as we didn't make mistakes with the hyphens and dashes, you know whether we're referring to the `template-project` repository or the `template_project` package/module.
