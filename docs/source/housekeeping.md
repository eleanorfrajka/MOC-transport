# Project Housekeeping Checklist

A quick checklist for maintaining the project environment, development tools, and CI/CD workflows.

---

## Adding a New Package

- ✅ Add to `requirements.txt` if it's needed at runtime.
- ✅ Add to `requirements-dev.txt` if it's only for development, testing, or documentation.
- ✅ If CI depends on it, confirm it’s included in GitHub Actions workflows.

## Updating Dependencies

- ✅ Specify minimum versions to maintain compatibility across environments.
- ✅ Test the update locally and in GitHub Actions.
- ✅ Optionally recreate your virtual environment for a clean state.

## Cleaning or Recreating the Environment

- ✅ Delete and recreate your virtual environment after major updates.
- ✅ Reinstall with `pip install -r requirements-dev.txt`.
- ✅ Run `pre-commit run --all-files` to ensure formatting and linting.
- ✅ Test with `pytest`.

## Pre-commit and Tests

- ✅ Add new hooks to `.pre-commit-config.yaml` if needed.
- ✅ Test new hooks locally with `pre-commit run --all-files`.
- ✅ Confirm CI passes.

## Documentation

- ✅ Ensure any new doc dependencies are in `requirements-dev.txt`.
- ✅ Test docs build locally using `make clean html` in the `docs/` directory.
- ✅ Confirm the GitHub Actions documentation build workflow passes.

## Before Merging a Branch

- ✅ Run `pytest` locally.
- ✅ Run `pre-commit run --all-files`.
- ✅ Confirm GitHub Actions CI passes.
- ✅ Optional: squash commits for a clean history.
    - When merging a pull request, select “Squash and merge” in the GitHub interface. This will combine all commits from the branch into a single, clean commit on main. You can (and should) edit the final commit message to describe the overall change clearly. Use squash for branches with multiple small commits or work-in-progress history. Skip squashing if you have meaningful, separated commits that you want to preserve in history.
---

*This checklist was drafted with the help of ChatGPT, in collaboration with the project developer.*

