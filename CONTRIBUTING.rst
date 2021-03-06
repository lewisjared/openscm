Contributing
============

Thanks for contributing to OpenSCM. We are always trying to improve this
tool, add new users and can do so even faster with your help!

Following the guidelines will help us work together as efficiently as
possible. When we all work with a common understanding, we can make sure
that issues are addressed quickly, suggested changes can be easily
assessed and pull requests can be finalised painlessly.

All contributions are welcome, some possible suggestions include:

-  bug reports (make a new issue and use the template please :D)
-  feature requests (make a new issue and use the template please :D)
-  pull requests (make a pull request and use the template please :D)
-  tutorials (or support questions which, once solved, result in a new
   tutorial :D)
-  improving the documentation

Please don’t use the repository to have discussions about the results.
Such discussions are scientific and generally belong in the scientific
literature, not in a development repository.


Ground Rules
************

As a contributor, it is vital that we all follow a few conventions:

-  Be welcoming to newcomers and encourage diverse new contributors from
   all backgrounds. See the :ref:`code_of_conduct`.
-  Create issues for changes and enhancements, this ensures that
   everyone in the community has a chance to comment
-  Ensure that you pass all the tests before making a pull request
-  Avoid pushing directly to master, all changes should come via pull
   requests


Setup
*****

Editor Config
~~~~~~~~~~~~~

The repository contains a ``.editorconfig`` file. This ensures that all
of our text editors behave the same way and avoids spurious changes
simply due to differing whitespace or end of line rules.

Many editors have built in support for ``Editorconfig`` but some require
a plugin. To work out if your editor requires a plugin, please check
https://editorconfig.org/.


Getting started
***************

Your First Contribution
~~~~~~~~~~~~~~~~~~~~~~~

The development methodology for OpenSCM makes heavy use of ``git``,
``make``, virtual environments and test driven development. If you
aren’t familiar with any of these terms it might be helpful to spend
some time getting up to speed on these technologies. Some helpful
resources (the longest take about 5 hours to work through):

-  `Introduction to git <https://swcarpentry.github.io/git-novice/>`__
   by Software Carpentry
-  `"Making a pull request" <http://makeapullrequest.com/>`__
-  `"My first pull request" <http://www.firsttimersonly.com/>`__
-  `Intoduction to tests
   <https://v4.software-carpentry.org/test/index.html>`__ by Software
   Carpentry and `"Getting started with mocking"
   <https://semaphoreci.com/community/tutorials/getting-started-with-mocking-in-python>`__
-  `Introduction to make
   <https://swcarpentry.github.io/make-novice/>`__ by Software
   Carpentry
-  Virtual environments with `venv
   <https://docs.python.org/3/library/venv.html>`__
-  `Continuous integration (CI)
   <https://docs.travis-ci.com/user/for-beginners/>`__; we use `Travis
   CI <https://travis-ci.com/>`_ for our CI but there are a number of
   good providers.
-  `Jupyter Notebooks
   <https://medium.com/codingthesmartway-com-blog/getting-started-with-jupyter-notebook-for-python-4e7082bd5d46>`__;
   we recommend simply installing ``jupyter`` (``conda install
   jupyter`` or ``pip install jupyter``) in your virtual environment.
-  Documentation generation with `Sphinx
   <http://www.sphinx-doc.org/en/master/>`__


Development workflow
********************

For almost all changes, there should be a corresponding `Pull
Request <https://github.com/openclimatedata/openscm/pulls>`__ (PR) on
GitHub to discuss the changes and track the overall implementation of
the feature. These PRs should use the PR template.

It is better to break a larger problem into smaller features if you
can. Each feature is implemented as a branch and merged into master
once all of the tests pass. This is development workflow is preferred
to one long-lived branch which can be difficult to merge.

The workflow for implementing a change to opencm is:

-  Create a PR. Initially you will not be ready to merge so prefix the
   title of the PR with ‘WIP:’.
-  Start a branch for the feature (or bug fix). When you start a new
   branch, be sure to pull any changes to master first.

   .. code:: bash

      git checkout master
      git pull
      git checkout -b my-feature

-  Develop your feature. Ensure that you run ``make test`` locally
   regularly to ensure that the tests still pass
-  Push your local development branch. This builds, tests and packages
   OpenSCM under Linux. The committer will be emailed if this process
   fails.
-  Before the PR can be merged it should be approved by another team
   member and it must pass the test suite. If you have a particular
   reviewer in mind, assign the PR to that user.
-  Your PR may need to be `rebased
   <https://www.atlassian.com/git/tutorials/rewriting-history/git-rebase>`__
   before it can be merged. Rebasing replays your commits onto the new
   master commit and allows you to rewrite history.

   .. code:: bash

      git fetch
      git checkout my-feature
      git rebase -i origin/master

-  Once approved, a maintainer can merge the PR.


Testing
*******

The tests are automatically run after every push using GitHub’s CI
pipelines. If the tests fail, the person who committed the code is
alerted via email.

Running the tests
~~~~~~~~~~~~~~~~~

To run the tests locally, simply run ``make test``. This will create an
isolated virtual environment with the required python libraries. This
virtual environment can be manually regenerated using ``make venv -B``.

Types of test
~~~~~~~~~~~~~

We have a number of different types of test:

-  unit, in the ``tests/unit`` folder
-  integration, in the ``tests/integration`` folder

Unit
^^^^

Unit tests test isolated bits of code, one at a time. Thus, they only
work if the tested functions are small and will almost inevitably
require the use of mocking. Their purpose is to help to isolate bugs
down to particular functions or lines of code.

Integration
^^^^^^^^^^^

Integration tests test a whole pipeline of functions on a higher level
than unit tests. They ensure that all our joins make sense when run
without (or with few) mocks. Overall, integration tests should
reproduce how a user would interact with the package.


Release Process
***************

We use tags to represent released versions of OpenSCM. Once you have
tagged a new release in our git respoitory, ``versioneer`` takes care of
the rest.

We follow `Semantic Versioning <https://semver.org/>`__, where version
strings are of the format vMAJOR.MINOR.PATCH. We follow these
conventions when deciding how to increment the version number, increment

-  MAJOR version when you make incompatible API changes,
-  MINOR version when you add functionality in a backwards-compatible manner
-  PATCH version when you make backwards-compatible bug fixes.

The steps undertaken to create a release are:

-  Checkout the latest commit in the master branch and ensure that your
   working copy is clean
-  Update ``CHANGELOG.rst`` to tag the unreleased items with the version
   and date of release. The unreleased section should now be empty.
-  Commit the changes with the message “Bumped to {}” where {} is
   replaced with the version string
-  Tag the commit with the version string. i.e. ``git tag v7.1.0``
-  Push the commit and tags ``git push; git push --tags``


Attribution
***********

Thanks to
https://github.com/nayafia/contributing-template/blob/master/CONTRIBUTING-template.md
for the template.
