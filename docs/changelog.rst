=========
Changelog
=========

----------------
Version 0 (Beta)
----------------

0.3.0 (2019-Jan-30)
===================

Feature Updates
---------------

* Extending the ``SubscriptionPlan`` model to include a short, plain-text
  description and a longer HTML description.
* Creating ``PlanList`` model to record group of ``SubscriptionPlan`` models
  to display on a single page for user selection.
* Creating a view and template to display the most recently created
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
