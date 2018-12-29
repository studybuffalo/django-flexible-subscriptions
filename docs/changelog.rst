=========
Changelog
=========

----------------
Version 0 (Beta)
----------------

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
