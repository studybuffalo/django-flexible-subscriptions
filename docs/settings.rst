========
Settings
========

Below is a comprehensive list of all the settings for
Django Flexible Subscriptions.

--------------
Admin Settings
--------------

These are settings to control aspects of the Django admin support.

``DSF_ENABLE_ADMIN``
====================

**Required:** ``False``

**Default (boolean):** ``False``

Whether to enable the Django Admin views or not.

-----------------
Currency Settings
-----------------

These are the settings to control aspects of currency repsentation.

``DSF_CURRENCY_LOCALE``
=======================

**Required:** ``False``

**Default (string):** ``en_us``

The currency locale to use for currency formatting. The following
formats are currently available:

* ``en_ca`` (Canada, English)
* ``en_us`` (United States of America, English)
* ``fr_ca`` (Canada, French)

Additional currencies can be easily added by adding to the ``CURRENCY``
dictionary in the ``conf`` module. Please make a pull request to add or
update a currency if needed.

-----------------
Template Settings
-----------------

These settings control aspects of the HTML templates.

``DFS_BASE_TEMPLATE``
=====================

**Required:** ``False``

**Default (string):** ``subscriptions/base.html``

Path to an HTML template that is the 'base' template for the site. This
allows you to easily specify the main site design for the provided
Django Flexible Subscription views. The template must include a
``content`` block, which is what all the templates override.
