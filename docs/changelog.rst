=========
Changelog
=========

----------------
Version 0 (Beta)
----------------

0.10.0 (2020-Feb-16)
====================

Feature Updates
---------------

* Switching ``ugettext_lazy`` to ``gettext_lazy`` (this function is
  being depreciated in Django 4.0).
* Adding a slug field to ``SubscriptionPlan``, ``PlanCost``, and
  ``PlanList`` models. This will make it easier to reference specific
  subscription details in custom views.

0.9.0 (2020-Jan-15)
===================

Feature Updates
---------------

* Adding currency support for (the Islamic Republic of) Iran.

Bug Fixes
---------

* Fixed issues where currency display could not handle non-decimal
  currencies.

0.8.1 (2019-Dec-25)
===================

Feature Updates
---------------

* Removes ``django-environ`` from development dependencies and switches
  functionality over to ``pathlib``.

Bug Fixes
---------

* Fixing bug with sandbox settings and Django 3.0 involving declaration
  of languages.
* Fixed issue where the ``RecurrenceUnit`` of the ``PlanCost`` model
  was trying to generate migration due to a change in the default
  value.

0.8.0 (2019-Dec-15)
===================

Feature Updates
---------------

* Removing official support for Django 2.1 (has reach end of life).
* Removing Tox from testing. Too many conflicting issues and CI system
  can handle this better now.

0.7.0 (2019-Dec-01)
===================

Feature Updates
---------------

* Switching ``PlanCost`` ``recurrence_unit`` to a CharField to make
  it more clear what the values represent.
* Adding ``PlanCost`` as an InlineAdmin field of ``SubscriptionPlan``.

0.6.0 (2019-Aug-19)
===================

Feature Updates
---------------

* Integrating subscription management utility functions into Django
  management commands. Documentation has been updated to explain this
  functionality.

0.5.0 (2019-Aug-18)
===================

Bug Fixes
---------

* Fixed issues where last billing date and end billing date were not
  diplaying properly when cancelling a subscription.
* Fixing the ``SubscribeUserList`` view to not show inactive
  subscriptions.

Feature Updates
---------------

* Improving styling for user-facing views and refactoring style sheet.
* Adding support for German (Germany) locale (``de_de``).

0.4.2 (2019-Aug-07)
===================

Bug Fixes
---------

* Resolving issue where subscription form would generate errors on
  initial display.
* Fixed bug where ``PlanList`` would display ``SubscriptionPlan``
  instances without associated `PlanCost` instances, resulting in
  errors on subscription order preview.

Feature Updates
---------------

* Streamlining the ``PlanList`` - ``PlanListDetail`` -
  ``SubscriptionPlan`` relationship to make relationships more apparent
  and easier to query.
* Added ``FactoryBoy`` factories to help streamline future test
  writing.
* Added validation of ``PlanCost`` ``UUID`` in the
  ``SubscriptionPlanCostForm`` to confirm a valid UUID is provided and
  return the object immediately.
* Updated ``PaymentForm to include validation of credit card numbers
  and CVV numbers and switched expiry months and years to
  ``ChoiceField`` to ensure valid data collected.

0.4.1 (2019-Aug-05)
===================

Bug Fixes
---------

* Adding ``styles.css`` to package data.

0.4.0 (2019-Aug-05)
===================

Feature Updates
---------------

* Adding responsive styling to all base HTML templates.
* Updating sandbox site to improve demo and testing functions.
* Breaking more template components into snippets and adding base
  templates to make it easier to override pages.
* Adding pagination to views to better handle long lists.
* Adding support for Django 2.2

0.3.2 (2019-Jul-17)
===================

Bug Fixes
---------

* Bug fixes with settings, sandbox site, and admin pages.


0.3.1 (2019-Jul-02)
===================

Feature Updates
---------------

* Adding Australian Dollars to available currencies.

0.3.0 (2019-Jan-30)
===================

Feature Updates
---------------

* Creating ``PlanList`` model to record group of ``SubscriptionPlan``
  models to display on a single page for user selection.
* Creating a view and template to display the the oldest active
  ``PlanList``.

0.2.1 (2018-Dec-29)
===================

Bug Fixes
---------

* Adding missing methods to ``SubscribeView`` and ``Manager`` to record
  payment transactions. Added additional method
  (``retrieve_transaction_date``) to help with transaction date
  specification. Reworked method calls around payment processing to
  streamline passing of arguments between functions to reduce need to
  override methods.
* Fixing issue in ``Manager`` class where the future billing date was
  based off the current datetime, rather than the last billed datetime.
* Adding method to update next billing datetimes for due subscriptions
  in the ``Manager`` class.
* Switching the default ``success_url`` for ``SubscribeView`` and
  ``CancelView`` to the user-specific list of their subscriptions,
  rather than the subscription CRUD dashboard.

0.2.0 (2018-Dec-28)
===================

Feature Updates
---------------
* Switching arguments for the ``process_payment`` call to keyword
  arguments (``kwargs``).
* Allow the ``SubscriptionView`` class to be specified in the settings
  file to make overriding easier.

Bug Fixes
---------

* Passing the PlanCostForm form into the process_payment call to
  allow access to the amount to bill.

0.1.1 (2018-Dec-28)
===================

Bug Fixes
---------

* Adding the ``snippets`` folder to the PyPI package - was not included
  in previous build.

0.1.0 (2018-Dec-26)
===================

Feature Updates
---------------

* Initial package release.
* Allows creation of subscription plans with multiple different costs
  and billing frequencies.
* Provides interface to manage admin functions either via the Django
  admin interface or through basic CRUD views.
* Provides user views to add, view, and cancel subscriptions.
* Templates can be customized by either specifying the base HTML
  template and extending it or overriding templates entirely.
* Template tags available to represent currencies on required locale.
* Manager object available to integrate with a Task Scheduler to manage
  recurrent billings of subscriptions.
* Sandbox site added to easily test out application functionality.
