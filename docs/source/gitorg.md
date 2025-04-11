Transferring to an Organisation
===============================

At some point, you may find it useful to transfer a repository from a personal Github account to an "organisation".  There isn't strictly a need to do this, but for a repository where you want wider community participation, it may reduce the barrier to someone suggesting edits.

Steps to transfer:

1. Set up a team in an Organisation that you're admin in (e.g., https://github.com/orgs/ifmeo-hamburg/teams/seagliderOG1-maintainers)

2. Go to settings on the repo, scroll down to "Danger Zone" and select "Transfer ownership", and transfer it to that organisation under the control of that team.

3. Head over to the new home of the repo (in the organisation) and check that everything moved properly (Issues, open pull requests, etc).

4. Go to settings: collaborators and check that everyone has the correct roles (e.g., "write" for team members)

5. Notify collaborators of the move

6. Go to Settings:github pages and check that the docs site is setup correctly

7. Go to the README and docs, and update links to the repo and docs site

8. Go to the package settings in `pyproject.toml` and update the URLs fo the repo and documentation that will display on PyPI

9. On PyPI: trusted publisher, update the repo address to where it is now for package publication

10. Do a new release to push all of these changes to PyPI and conda-forge

11. Special case for the original owner: Now fork the new repository since https://github.com/eleanorfrajka/seagliderOG1 won't exist.
