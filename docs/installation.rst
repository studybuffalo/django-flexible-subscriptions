===============
Getting started
===============

----------------------
Installation and Setup
----------------------

Install django-flexible-subscriptions and its dependencies
==========================================================

Install ``django-flexible-subscriptions`` (which will install  Django
as a dependency). It is strongly recommended you use a virtual
environment for your projects. For example, you can do this easily
with Pipenv_:

.. code-block:: shell

    $ pipenv install django-flexible-subscriptions

.. _Pipenv: https://pipenv.readthedocs.io/en/latest/

Add django-flexible-subscriptions to your project
=================================================

1. Add ``django-flexible-subscriptions`` to your settings file:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'subscriptions',
        ...
    ]


2. Run the package migrations:

.. code-block:: shell

    $ pipenv run python manage.py migrate

3. Add the ``django-flexible-subscriptions`` URLs to your project:

.. code-block:: python

    urlpatterns = [
        ...
        url(r'^subscriptions/', include('subscriptions_urls')),
        ...
    ]

4. You can test that the project is properly setup by running the
   server (``pipenv run python manage.py runserver``) and visiting
   ``http://127.0.0.1:8000/subscriptions/subscribe/``.

-------------
Configuration
-------------

While not required, you are able to customize aspects of Django
Flexible Subscriptions in your settings file. At a minimum, you will
probably want to set the following settings:

.. code-block:: python

    # Set your currency type
    DFS_CURRENCY_LOCALE = 'en_us'

    # Specify your base template file
    DFS_BASE_TEMPLATE = 'base.html'

A full list of settings and their effects can be found in the
:doc:`settings documentation</settings>`.

--------------------
Setup a Subscription
--------------------

Once Django Flexible Subscriptions is setup and running, you will be
able to add your first subscription.

.. note::

    You will need an account with staff/admin access to proceed with
    the following steps. All referenced URLs assume you have added
    the ``django-flexible-subscriptions`` URLs at ``/subscriptions/``.


-----------------------------
Considerations for Production
-----------------------------

When moving Django Flexible Subscriptions to a production environment,
you will probably want to consider the following:

* ``django-flexible-subscriptions`` comes with its own ``styles.css``
  file - you will need to ensure you run the ``collectstatic``
  management command if you have not overriden it with yoru own file.
