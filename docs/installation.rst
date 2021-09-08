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
   as well (see Understanding a Subscription Plan for details).

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
    from django.urls import include, urls


    urlpatterns = [
        ...
        path('subscriptions/', include('subscriptions.urls')),
        path('admin/', include(admin.site.urls), # Optional, but recommended
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

* **Recurrence period**: How often the plan is billed per recurrence
  unit.
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

--------------------------------------
Understanding a Subscription Plan List
--------------------------------------

Django Flexible Subscriptions provides basic support to add a
"Subscribe" page to your site to allow users to select a subscription
plan. The plans listed on this page are controlled by the ``PlanList``
model. The ``PlanList`` model includes the following details:

* **Title**: A title to display on the page (may include HTML content).
* **Subttile**: A subtitle to display on the page (may include HTML
  content).
* **Header**: Content to display before the subscription plans are
  listed (may include HTML content).
* **Header**: Content to display after the subscription plans are
  listed (may include HTML content).
* **Active**: Whether this list is active or not.

.. note::

    The first active ``PlanList`` instance is used to populate the
    subscribe page. You will need to inactivate or delete older
    ``PlanList`` instances if you want a newer one to be used.

Once a ``PlanList`` is created, you will be able to associate ``Plan``
instances to specify the following details:

* **HTML content**: How you want the plan details to be presented
  (may include HTML content).
* **Subscribe button text**: The text to display on the "Subscribe"
  button at the end of the plan description.

--------------------
Creating a Plan List
--------------------

Once you have created you subscription plan, you can create your
``PlanList``.

1. Visit ``/subscriptions/dfs/`` to access the **Developer Dashboard**.

2. Click the **Plan lists** button or visit
   ``/subscriptions/dfs/plan-lists/``.  Click on the **Create a new
   plan list** button.

3. Fill in the plan list details and click the **Save** button.

4. To add ``Plan`` instances to your ``PlanList`` click the **Manage
   plans** button on the Plan Lists page.

5. Click on the **Add plan** button, fill in the desired details and
   click the **Save** buton.

6. You can now visit ``/subscriptions/subscribe/`` to see your plan
   list.

----------
Next Steps
----------

If you completed all the steps above, you should now have a working
subscription system on your development server. You will likely want
to add payment handling and a task runner to automate subscription
renewals and expiries. Instructions and examples for this can be found
the :doc:`Advanced usage</advanced>` section.

-----------------------------
Considerations for Production
-----------------------------

When moving Django Flexible Subscriptions to a production environment,
you will probably want to consider the following:

* ``django-flexible-subscriptions`` comes with its own ``styles.css``
  file - you will need to ensure you run the ``collectstatic``
  management command if you have not overriden it with your own file.
* The ``SubscribeView`` included with ``django-flexible-subscriptions``
  is intended to be extended to implement payment processing. The base
  view will automatically approve all payment requests and should be
  overriden if this is not the desired behaviour.
* ``django-flexible-subscriptions`` includes management commands to
  assist with managing subscription renewals and expiries. While these
  can be ran manually, you should consider implementing some task
  manager, such as ``cron`` or ``celery``, to run these commands on a
  regular basis.
