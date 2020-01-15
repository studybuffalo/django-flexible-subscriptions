========
Settings
========

Below is a comprehensive list of all the settings for
Django Flexible Subscriptions.

--------------
Admin Settings
--------------

These are settings to control aspects of the Django admin support.

``DFS_ENABLE_ADMIN``
====================

**Required:** ``False``

**Default (boolean):** ``False``

Whether to enable the Django Admin views or not.

-----------------
Currency Settings
-----------------

These are the settings to control aspects of currency repsentation.

``DFS_CURRENCY_LOCALE``
=======================

**Required:** ``False``

**Default (string):** ``en_us``

The currency locale to use for currency formatting. The following
formats are currently available:

* ``de_de`` (Germany, German)
* ``en_au`` (Australia, English)
* ``en_ca`` (Canada, English)
* ``en_us`` (United States of America, English)
* ``fa_ir`` (Iran, Persian)
* ``fr_ca`` (Canada, French)

Additional currencies can be easily added by adding to the ``CURRENCY``
dictionary in the ``conf`` module. Please make a pull request to add or
update a currency if needed.

------------------------
View & Template Settings
------------------------

These control various aspects of HTML templates and Django views.

``DFS_BASE_TEMPLATE``
=====================

**Required:** ``False``

**Default (string):** ``subscriptions/base.html``

Path to an HTML template that is the 'base' template for the site. This
allows you to easily specify the main site design for the provided
Django Flexible Subscription views. The template must include a
``content`` block, which is what all the templates override.

``DFS_SUBSCRIBE_VIEW``
======================

**Required:** ``False``

**Default (string):** ``subscriptions.views.SubscribeView``

The path to the SubscribeView to use with
``django-flexible-subscriptions``. This will generally be set to a
class view the inherits from ``SubscribeView`` to allow customization
of payment and subscription processing.

------------------------
View & Template Settings
------------------------

These control various aspects of the management commands.

``DFS_MANAGER_CLASS``
======================

**Required:** ``False``

**Default (string):** ``subscriptions.management.commands._manager.Manager``

The path to the ``Manager`` object to use with the management commands.
This will generally be set to a class that inherits from the
``django-flexible-subscriptions`` ``Manager`` class to allow
customization of renewal billings and user notifications.
