=========
Changelog
=========

----------------
Version 0 (Beta)
----------------

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
