# Contributing to this project

## Basic workflow

The upstream main repository is located at: [https://github.com/AMOCcommunity/amocarray](https://github.com/AMOCcommunity/amocarray), and you would like to contribute to it.

When you first work with a shared repository, you will want to follow the steps below.  Note that many of these are given as examples using GitHub.com.  If you prefer to use the command line, that also works.

### 1. Fork the repository

**On Github.com:** Fork the repository into your own Github account.  If prompted, specify that you would like to contribute to the original project.  

Now you have a separate version of the repository, your "forked main" at `https://github.com/YOUR_USERNAME/amocarray`

### 2. Clone your fork to your computer

**On Github.com:** From your forked repository, clone the repository to your computer.  

(i) Navigate to your repositories on GitHub, `https://github.com/YOUR_USERNAME/amocarray`.  Click the green `<> Code` dropdown button, and choose a method to clone this.  If you're not familiar with cloning repositories to your computer, choose `Open with Github Desktop` which will require you to have the application "GitHub Desktop" on your computer.  

(ii) When prompted, choose where on your computer you would like this to live (`/a/path/on/your/computer/`).  

> **Tip**
> If you use a cloud backup service, you may find it is recommended to *not* put this in a folder that is synced with the cloud. This is because the online backups via a cloud service will need to keep copying files back and forth when you switch branches (which replaces the files in your active directory with the versions from each branch), and depending on timing, the synchronisation could cause errors or duplication.  Additionally, using git negates much of the need for cloud backups as local commits *and* pushes to the online git repository provides backups by design.

### 3. Find the clone on your computer

**On your computer in File Explorer (Windows) or Finder (Mac):** Now you have a copy of the repository on your computer, with the associated "git" tracking information.  The repository already knows the history of changes, and has the necessary structure to update.  These are in a hidden folder within the repository folder (likely called `/a/path/on/your/computer/amocarray/.git`).   

This is your **forked main**, now at `https://github.com/YOUR_USERNAME/amocarray` and on your local computer at `/a/path/on/your/computer/amocarray/`.  The **upstream main** is where the project originated.  In this example, [https://github.com/AMOCcommunity/amocarray](https://github.com/AMOCcommunity/amocarray).

### 4. Create a branch for edits

**On your computer in a terminal window:** When you'd like to start making changes in your repository, it's best practice to do this not in your **forked main** but instead in a **branch of your fork**.  This is a separate copy of your forked main, which diverges or branches from the forked main at the point when you create the branch.  In this example here, a forked repository from someone else's (AMOCcommunity's) upstream main, you will never work directly on your **forked main**.

To make a branch, at the command line, the series of steps would be (from within `/a/path/on/your/computer/amocarray/`):
```
$ git checkout main
$ git pull
$ git checkout -b yourname-patch-1
```
where you change "yourname" to your first name (or other useful identifier, e.g. your GitHub username).

This branch will now be up-to-date with the latest changes within `main` (which is what the `git pull` command does), but will have a separate copy for you to make your edits in.

> **Suggested naming convention:** `yourfirstname-patch-#` where `#` increments by one for each new branch you make.  Some people also name branches by the topic or issue that branch is addressing.  So far, I've found for early code development that I'll intend a branch for one purpose, but find another that should be fixed/changed first, and then I have a branch name called `eleanor-docs-1` but it's really about a new test of plotters (or something).

### 5. Make an edit in the branch

**On your computer in VS Code (or wherever you work on Python):** Make a change to a file.  Even adding an extra line of whitespace will do this.  Then save the file.

### 6. Commit the change in your branch

**In VS Code**, to commit the change, you will navigate to the "source explorer" in the left hand bar, and add a commit message (text box above the blue "Commit" button).  This should be short, explaining in present tense what the commit does.

> **Optional (recommended):** Add a short code at the beginning of the commit message (one word) to help categorise what the commit is doing.  See [https://dev.to/ashishxcode/mastering-the-art-of-writing-effective-github-commit-messages-5d2p](https://dev.to/ashishxcode/mastering-the-art-of-writing-effective-github-commit-messages-5d2p).  

> Options include things like:

> - `feat: <extra text explaining more detail>` when you're adding a new feature or functionality
> - `fix: <extra text explaining more detail>` when you're committing a fix for a specific problem or issue
> - `style:` when you're making changes to style or formatting but not functionality (user should experience no change)
> - `refactor:` changes to the code that improve structure or organisation, but don't add features or fix bugs
> - `test:` when you're adding or updating tests for the code
> - `chore:` updating changes to the build process or other tasks not directly related to the code (e.g., GitHub workflows)
> - `perf:` Changes to improve code performance, e.g. speed
> - `ci:` changes to the continuous integration process

This stores the changes in your `/a/path/on/your/computer/amocarray/.git`.  The next steps (7-9) are to transmit those updates to the **upstream main**.

### 7. Create a pull request to upstream

**On your computer in VS Code:** Sync the commit to main.  If this is the first time you've done this from your branch, you will need to set the upstream.  Set the upstream to be `https://github.com/AMOCcommunity/amocarray`.  This will direct the pull request to the **upstream main** repository (not your **forked main**).  

### 8. Compare pull request on GitHub.com

**On Github.com (original repository):** Navigate to the original repository `https://github.com/AMOCcommunity/amocarray` and you should see the pull request has come through.  There will be a shaded bar at the top with a button "compare and pull request".  Click this button and on the next page add some useful details for the rest of the contributors to understand what your commit is doing.  

Note that the default version of this template includes some tests to be run when you submit a pull request.  The python code for these tests is located in `tests/`.  The Github Actions "workflow" that calls the tests is in `.github/workflows/tests.yml`.  See the next section of the documents about how to deal with these.

### 9. Merge the pull request

**On Github.com (original repository):** Navigate to the original repository [https://github.com/AMOCcommunity/amocarray](https://github.com/AMOCcommunity/amocarray).  Once your edits have passed all tests, been reviewed by a repository owner (if required) and approved, then you (as the creator of the pull request) can "merge".   This will push your changes from your **branch of your fork** onto the **upstream main**.  

### 10. Rinse and repeat

Now the upstream main has been updated.  To get ready for future changes, you'll want to:

- Sync your forked main with the upstream main
- Checkout main and pull changes
- Create a new branch for the next changes

**On Github.com (your forked repository):** If you want to make further changes *after a merge (by anyone)*, you should **first** sync your fork (main branch) to the origin.  

1. On your forked repository main, `https://github.com/yourGitHubUsername/template-project` where you should see a notification across the top saying "this is behind the origin/main by X commits" with the option to click the **sync** button.  Click it!  This gets your forked main branch _on Github_ up-to-date with the origin/main.

2. **On your computer, terminal window:** After syncing your fork to the origin's main on GitHub.com, the next step is to pull any new changes onto your fork's main branch _on your computer_.

```
$ git checkout main
$ git pull
```

3. **On your computer, terminal window:** Now you need to create a new branch for working _on your computer_.  
As before, create a new branch using `git checkout -b branchname` as in:
```
$ git checkout -b yourname-patch-2
```
This will create a new branch `yourname-patch-2` based on the new, updated main on your computer.  The `-b` option creates a branch (without `-b`, it will try to switch to a branch with that name).

Now you're ready to repeat from step 5.

> **Note:** If you forgot to sync your fork (main branch), and then have a new pull request, you may have merge have conflicts when pulling any changes to the main/origin.

