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

.. _settings-dfs_currency:

``DFS_CURRENCY``
================

**Required:** ``False``

**Default (string):** ``en_us``

The currency to use for currency formating. You may either specify a
``str`` value for the language code you want to use or a ``dict`` value
that declares all the required monetary conventions.

The following ``str`` values are available:

* ``de_de`` (Germany, German)
* ``en_au`` (Australia, English)
* ``en_ca`` (Canada, English)
* ``en_us`` (United States of America, English)
* ``fa_ir`` (Iran, Persian)
* ``fr_ca`` (Canada, French)
* ``fr_ch`` (Swiss Confederation, French)
* ``fr_fr`` (France, French)
* ``it_it`` (Itality, Italian)
* ``pl_pl`` (Republic of Poland, Polish)
* ``pt_br`` (Federative Republic of Brazil, Portuguese)
* ``en_in`` (India, English)
* ``en_ph`` (Philippines, English)
* ``en_gb`` (Great Britain, English)

Additional values can be added by submitting a pull request with the
details added to the ``CURRENCY`` dictionary in the
``subscriptions.currency`` module.

To specify a custom format, you can specify the following details
in a dictionary:

* ``currency_symbol`` (``str``): The symbol used for this currency.
* ``int_currency_symbol`` (``str``): The symbol used for this currency
  for international formatting.
* ``p_cs_precedes`` (``bool``): Whether the currency symbol precedes
  positive values.
* ``n_cs_precedes`` (``bool``): Whether the currency symbol precedes
  negative values.
* ``p_sep_by_space`` (``bool``): Whether the currency symbol is
  separated from positive values by a space.
* ``n_sep_by_space`` (``bool``): Whether the currency symbol is
  separated from negative values by a space.
* ``mon_decimal_point`` (``str``): The character used for decimal points.
* ``mon_thousands_sep`` (``str``): The character used for separating
  groups of numbers.
* ``mon_grouping`` (``int``): The number of digits per groups.
* ``frac_digits`` (``int``): The number of digits following the decimal
  place. Use 0 if this is a non-decimal currency.
* ``int_frac_digits`` (``str``): The number of digits following the
  decimal place for international formatting. Use 0 if this is a
  non-decimal currency.
* ``positive_sign`` (``str``): The symbol to use for the positive sign.
* ``negative_sign`` (``str``): The symbol to use for the negative sign.
* ``p_sign_posn`` (``str``): How the positive sign should be positioned
  relative to the currency symbol and value (see below).
* ``n_sign_posn`` (``str``): How the positive sign should be positioned
  relative to the currency symbol and value (see below).

The sign positions (``p_sign_posn`` and ``p_sign_posn``) use the
following values:

* ``0``: Currency and value are surrounded by parentheses.
* ``1``: The sign should precede the value and currency symbol.
* ``2``: The sign should follow the value and currency symbol.
* ``3``: The sign should immediately precede the value.
* ``4``: The sign should immediately follow the value.

``DFS_CURRENCY_LOCALE``
=======================

Deprecated - use :ref:`settings-dfs_currency` instead.

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
