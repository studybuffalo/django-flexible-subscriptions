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

1. Update ``django-flexible-subscriptions`` to your settings file.
   While not mandatory, it is very likely you will also want to include
   the ``django.contrib.auth`` and ``django.contrib.admin`` apps
   as well (see Understanding a Description Plan for details).

.. code-block:: python

    INSTALLED_APPS = [
        # Django applications
        'django.contrib.auth',
        'django.contrib.admin',
        ...
        # Your third party applications
        'subscriptions',
        ...
    ]

2. Run the package migrations:

.. code-block:: shell

    $ pipenv run python manage.py migrate

3. Add the ``django-flexible-subscriptions`` URLs to your project:

.. code-block:: python

    import subscriptions
    from django.contrib import admin # Optional, but recommended

    urlpatterns = [
        ...
        url(r'^subscriptions/', include('subscriptions_urls')),
        url(r'^admin/', include(admin.site.urls), # Optional, but recommended
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

---------------------------------
Understanding a Subscription Plan
---------------------------------

Django Flexible Subscriptions uses a ``Plan`` model to describe a
subscription plan. A ``Plan`` describes both billing details and
user permissions granted.

User permissions are dictacted by the Django ``Group`` model, which is
included as part of the authentication system. Django Flexible
Subscriptions will add or remove a ``Group`` from a ``User`` based on
the status of the user subscription. You may specify the permissions
the ``User`` is granted by associating them to that Group and running any
permission checks as needed. See the `Django documenation on "User
authentication in Django"`_ for more details. If you do not need to
grant a user permissions with a subscription, you may ignore the
``Group`` model.

.. _Django documenation on "User authentication in Django": https://docs.djangoproject.com/en/dev/topics/auth/

A subscription ``Plan`` contains the following details to dictate
how it functions:

    * **Plan name**: The name of the subscription plan. This will be
      displayed to the end user in various views.
    * **Plan description**: An optional internal description to help
      describe or differentiate the plan for the developer. The end user
      does not see this.
    * **Group**: The ``Group`` model(s) associated to this plan.
    * **Tag**: Custom tags associated with this plan. Can be used to
      organize or categorize related plans.
    * **Grade period**: The number of days a subscription will remain
      active for a user after a plan ends (e.g. due to non-payment).
    * **Plan cost**: Describes the pricing details of the plan.

One or more ``PlanCost`` models may be associated to a ``Plan``. This
allows you to offer the same plan at difference prices depending on
how often the billing occurs. This would commonly be used to offer a
discounted price when the user subscribes for a longer period of time
(e.g. annually instead of monthly). A ``PlanCost`` will contain the
following details:

    * **Recurrence period**: How often the plan is billed per
      recurrence unit.
    * **Recurrence unit**: The unit of measurement for the recurrence
      period. ``one-time``, ``second``, ``minute``, ``hour``, ``day``,
      ``week``, ``month``, and ``year`` are supported.
    * **Cost**: The amount to charge at each recurrence period.

-------------------------
Setup a Subscription Plan
-------------------------

Once Django Flexible Subscriptions is setup and running, you will be
able to add your first subscription.

.. note::

    You will need an account with staff/admin access to proceed with
    the following steps. All referenced URLs assume you have added
    the ``django-flexible-subscriptions`` URLs at ``/subscriptions/``.

1. Visit ``/subscriptions/dfs/`` to access the **Developer Dashboard**.

2. Click the **Subscription plans** link or visit
``/subscriptions/dfs/plans/``. Click on the **Create new plan** button.

3. Fill in the plan details and click the **Save** button.

-----------------------------
Considerations for Production
-----------------------------

When moving Django Flexible Subscriptions to a production environment,
you will probably want to consider the following:

* ``django-flexible-subscriptions`` comes with its own ``styles.css``
  file - you will need to ensure you run the ``collectstatic``
  management command if you have not overriden it with yoru own file.
