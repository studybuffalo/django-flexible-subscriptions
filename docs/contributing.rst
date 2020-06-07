============
Contributing
============

Contributions or forking of the project is always welcome. Below will
provide a quick outline of how to get setup and things to be aware of
when contributing.

----------------
Reporting issues
----------------

If you simply want to report an issue, you can use the
`GitHub Issue page`_.

.. _GitHub Issue page: https://github.com/studybuffalo/django-flexible-subscriptions/issues

--------------------------------------
Setting up the development environment
--------------------------------------

This package is built using Pipenv_, which will take care of both
your virtual environment and package management. If needed, you can
install ``pipenv`` through ``pip``::

    $ pip install pipenv

.. _Pipenv: https://pipenv.readthedocs.io/en/latest/

To download the repository from GitHub via ``git``::

    $ git clone git://github.com/studybuffalo/django-flexible-subscriptions.git

You can then install all the required dependencies by changing to the
package directory and installing from ``Pipfile.lock``::

    $ cd django-flexible-subscriptions
    $ pipenv install --ignore-pipfile --dev

Finally, you will need to build the package::

    $ pipenv run python setup.py develop

You should now have a working environment that you can use to run tests
and setup the sandbox demo.

-------
Testing
-------

All pull requests must have unit tests built and must maintain
or increase code coverage. The ultimate goal is to achieve a code
coverage of 100%. While this may result in some superfluous tests,
it sets a good minimum baseline for test construction.

Testing format
==============

All tests are built with the `pytest framework`_
(and `pytest-django`_ for Django-specific components). There are no
specific requirements on number or scope of tests, but at a bare
minimum there should be tests to cover all common use cases. Wherever
possible, try to test the smallest component possible.

.. _pytest framework: https://docs.pytest.org/en/latest/

.. _pytest-django: https://pytest-django.readthedocs.io/en/latest/

Running Tests
=============

You can run all tests with the standard ``pytest`` command::

    $ pipenv run py.test

To check test coverage, you can use the following::

    $ pipenv run py.test --cov=subscriptions --cov-report=html

You may specify the output of the coverage report by changing the
``--cov-report`` option to ``html`` or ``xml``.

Running Linters
===============

This package makes use of two linters to improve code quality:
`Pylint`_ and `pycodestyle`_. Any GitHub pull requests must pass all
Linter requirements before they will be accepted.

.. _Pylint: https://pylint.org/

.. _pycodestyle: https://pypi.org/project/pycodestyle/

You may run the linters within your IDE/editor or with the following
commands::

    $ pipenv run pylint subscriptions/ sandbox/
    $ pipenv run pylint tests/ --min-similarity-lines=12
    $ pipenv run pycodestyle --show-source subscriptions/ sandbox/ tests/

Of note, tests have relaxed rules for duplicate code warnings. This is
to minimize the level of abstraction that occurs within the tests with
the intent to improve readability.

----------------------
Updating documentation
----------------------

All documentation is hosted on `Read the Docs`_ and is built using
Sphinx_. All the module content is automatically built from the
docstrings and the `sphinx-apidoc`_ tool and the
`sphinxcontrib-napoleon`_ extension.

.. _Read the Docs: https://readthedocs.org/
.. _Sphinx: http://www.sphinx-doc.org/en/master/
.. _sphinx-apidoc: http://www.sphinx-doc.org/en/stable/man/sphinx-apidoc.html
.. _sphinxcontrib-napoleon: https://sphinxcontrib-napoleon.readthedocs.io/en/latest/

Docstring Format
================

The docstrings of this package follow the `Google Python Style Guide`_
wherever possible. This ensures proper formatting of the documentation
generated automatically by Sphinx. Additional examples can be found on
the `Sphinx napoleon extension documentation`_.

.. _Google Python Style Guide: https://github.com/google/styleguide/blob/gh-pages/pyguide.md
.. _Sphinx napoleon extension documentation: https://sphinxcontrib-napoleon.readthedocs.io/en/latest/

Building package reference documentation
========================================

The content for the Package reference is built using the
``sphinx-apidoc`` tool. If any files are added or removed from the
``subscriptions`` module you will need to rebuild the
``subscriptions.rst`` file for the changes to populate on Read
the Docs. You can do this with the following command::

    $ pipenv run sphinx-apidoc -fTM -o docs subscriptions subscriptions/migrations subscriptions/urls.py subscriptions/apps.py subscriptions/admin.py

Linting documentation
=====================

If you are having issues with the ReStructuredText (reST) formatting,
you can use ``rst-lint`` to screen for syntax errors. You can run a
check on a file with the following::

    $ pipenv run rst-lint /path/to/file.rst

--------------------
Distributing package
--------------------

Django Flexible Subscriptions is designed to be distributed with PyPI.
While most contributors will not need to worry about uploading to PyPI,
the following instructions list the general process in case anyone
wishes to fork the repository or test out the process.

.. note::

    It is recommended you use `TestPyPI`_ to test uploading your
    distribution while you are learning and seeing how things work. The
    following examples below will use TestPyPI as the upload target.

.. _TestPyPI: https://test.pypi.org/

To generate source archives and built distributions, you can use the
following::

    $ pipenv run python setup.py sdist bdist_wheel

To upload the distributions, you can use the following ``twine``
commands::

    $ pipenv run twine upload --repository-url https://test.pypi.org/legacy/ dist/*

You will need to provide a PyPI username and password before the upload
will start.
