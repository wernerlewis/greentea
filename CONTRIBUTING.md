# Contributing

We appreciate your contributions! Because this is an open source project, we want to keep it as easy as possible to contribute changes. However, we need contributors to follow a few guidelines.

## Enhancements and bugs

Enhancements are:

* New features implementation.
* Code refactoring.
* Coding rules or coding style improvements.
* Code comments improvement.
* Documentation work.

Bugs are:

* Issues that application users and the ARM mbed team raise.
* Issues the ARM mbed team creates internally from the Continuous Integration pipeline and build servers.
* Issues that developers and the ARM mbed team detect using automation tools, such as compilers, sanitizers, static code and analysis tools.

## Workflow

### Forking and cloning this repository

First [fork](https://help.github.com/articles/fork-a-repo/) this repository in GitHub. Then, clone it locally with:

```
$ git clone <repo-link>
```

Now, you can create separate branches in the forked repository and prepare pull requests with changes.

### Issues solving

To solve issues, follow the steps below:

1. A user (any user) files an issue.
1. A gate-keeper assigns a proper label to the issue.
1. A user who wants to fix the issue, the bug fixer, forks and clones the repository.
1. Optional: the bug fixer asks for and receives clarifications using the Issues tab's Comment section.
1. The bug fixer creates a pull request that fixes the issue.
1. Others review the pull request.
1. The bug fixer handles all code review comments.
1. A gate-keeper accepts the pull request.
1. The pull request merges successfully.

### Code review

The code review process catches both style and domain-specific issues. It also follows and respects the _definition of done_. Please make sure your code follows the style of the source code you are modifying. A gate-keeper must review each pull request before we can merge the pull request to the master branch.

## Issues and bug reporting

Please report all bugs using the Issues tab on the GitHub page. This process helps us collaborate on issues promptly. One of our gate-keepers (developers responsible for quality and the repository) will review the issue and assign a label, such as _bug_, _enhancement_, _help wanted_ or _wontfix_.

## How to contribute

You can file a bug, help fix a bug or propose a new feature (or enhancement) and implement it yourself. If you want to contribute, please see below:

* Bug reports: File a bug report in the Issues tab of this repo to let us know there are problems with the code.
  * Make sure your bug report contains a simple description of the problem.
  * Include information about the host computer's configuration and OS or VM used.
  * Include information about the application's version. All applications should have at least a `--version` switch you can use to check the version.
  * Copy and paste useful console dumps and configuration files' content. Please use [fenced code blocks](https://help.github.com/articles/basic-writing-and-formatting-syntax/#quoting-code) to encapsulate code snippets.
* New features or bug fix: Create a pull request with your changes.
* General feedback: Give feedback by posting comments on existing pull requests and issues.

### Simple workflow for bug fixes

* Select an issue to fix from open issues.
* Fork the repository you wish to modify.
* Locally clone your fork, and create a separate branch to fix the issue.

Note: In this example we will fix issue #38.

```
$ git clone <fork-repo-link>
$ git checkout -b issue_38
... add changes locally to fix an issue
```

* Add and commit your changes.

```
$ git add .
$ git commit -m "Add fix for issue #38" -m "More verbose explanation of the change/fix"
$ git push origin issue_38

```

* Push changes to GitHub.
* Create pull request from GitHub (your fork's dashboard).

### Branch naming conventions

We prefer you use a standard naming convention when creating pull requests. Here are a few examples of branch name prefixes you could use when creating a pull request from your fork:

* `issue_` - branch with fix for issue. For example, `issue_38`.
* `doc_` - documentation update. For example, `doc_add_faq`.
* `devel_` - development of a new feature. For example, `devel_udp_client_test`.
* `test_` - when pull request will consist of only new/updates to test cases. For example, `test_paralllel_execution`.

## Coding style and coding rules

This chapter attempts to explain the basic styles and patterns in mbed test tools projects. Do the following to produce new code and update existing code.

### Code like a Pythonista: idiomatic Python

Please do your best to follow the [Idiomatic Python](http://python.net/~goodger/projects/pycon/2007/idiomatic/handout.html) interactive tutorial.

### Style guide for Python code

Please see [PEP 0008 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/) for details.

### Whitespace

* 4 spaces per indentation level.
* No hard tabs.
* Never mix tabs and spaces.
* One blank line between functions.
* Two blank lines between classes.
* No whitespace at the end of a line.

* Add a space after "," in dicts, lists, tuples and argument lists, and after ":" in dicts, but not before.
* Put spaces around assignments and comparisons (except in argument lists).
* No spaces just inside parentheses or just before argument lists.
* No spaces just inside docstrings.

Example:

```python
def make_squares(key, value=0):
    """! Return a dictionary and a list...
    @param value Value parameter with default value of zero (0)
    @return Retruns tuple of 'd' stuff and 'l' stuff
    """
    d = {key: value}
    l = [key, value]
    return d, l
```

### Naming

* `joined_lower` for functions, methods, attributes.
* `joined_lower` or ALL_CAPS for constants.
* `StudlyCaps` for classes.
* `camelCase` only to conform to pre-existing conventions.
* Attributes: `interface`, `_internal`, `__private`
* Try to avoid the `__private` form.

## Checking code style

We use [flake8](http://flake8.pycqa.org/en/latest/index.html) to enforce our style conventions. You can check your code style by running `flake8` from your command line in the root project directory.

## Testing and code coverage

The application should be unit tested (at least a minimal set of unit tests should be implemented in the `/test` directory). We should be able to measure the unit test code coverage.

Run a unit test suite to make sure your changes do not break current implementation:

```
$ cd <package>
$ python setup.py test
```

## Code coverage

To measure application code coverage for unit tests, please use the coverage tool. This set of commands locally creates a code coverage report for all unit tests:

```
$ cd <package>
$ coverage run setup.py test
$ coverage report
$ coverage html
```

The last command generates an HTML code coverage report. You can use it to check which parts of your code are not unit tested.

## Keep your GitHub fork updated

To fork a GitHub repo SOME_REPO/appname to USER/appname and keep it updated, please use the following steps.

### Track changes

```
$ git clone git@github.com:USER/appname.git
$ cd appname
$ git remote add upstream git@github.com:SOME_REPO/appname.git
```

### Verify:

Verify with the following:

```
$ git remote -v
origin  https://github.com/USER/appname.git (fetch)
origin  https://github.com/USER/appname.git (push)
upstream  https://github.com/SOME_REPO/appname.git (fetch)
upstream  https://github.com/SOME_REPO/appname.git (push)
```

### Update

To update, do the following from the local master branch:

```
$ git fetch upstream
$ git rebase upstream/master
```

Rebasing creates a cleaner history for developers with local changes or commits.

## Final notes

1. Please do not change the version of the package in the `setup.py` file. The person or process responsible for releasing will do this and release the new version.
2. Keep your GitHub fork updated! Please make sure you are rebasing your local branch with changes, so it is up to date and we can automatically merge your pull request.
3. If possible, please squash your commits before pushing to the remote repository.
4. Please, as part of your pull request:
  * Update `README.md` if your changes add new functionality to the module.
  * Add unit tests to the `/test` directory to cover your changes or new functionality.
