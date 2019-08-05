==============
Advanced usage
==============

-----------------------------
Changing styles and templates
-----------------------------

It is possible to override any component of the user interface by
overriding the style file or the templates. To override a file, simply
create a file with the same path noted in the list below.

It is also possible to setup your ``django-flexible-subscriptions``
to use a base template already in your project via your settings. See
the :doc:`settings</settings>` section for more details.

* **Core Files and Templates**

  * ``static/subscriptions/styles.css``
    (controls all template styles)
  * ``templates/subscriptions/base.html``
    (base template that all templates inherit from)
  * ``templates/subscriptions/subscribe_list.html``
    (user-facing; list and sign up for subscription plans)
  * ``templates/subscriptions/subscribe_preview.html``
    (user-facing; preview of subscription plan signup)
  * ``templates/subscriptions/subscribe_confirmation.html``
    (user-facing; confirmation of subscription plan signup)
  * ``templates/subscriptions/subscribe_thank_you.html``
    (user-facing; thank you page on successful subscription plan
    singup)
  * ``templates/subscriptions/subscribe_user_list.html``
    (user-facing; list of a user's subscriptions)
  * ``templates/subscriptions/subscribe_cancel.html``
    (user-facing; confirm cancellation of subscription)

* **Developer-Facing Templates**

  * ``templates/subscriptions/base_developer.html``
    (base template that all developer dashboard templates inherit from)
  * ``templates/subscriptions/dashboard.html``
    (developer-facing; dashboard template)
  * ``templates/subscriptions/plan_list.html``
    (developer-facing; list of all subscription plans)
  * ``templates/subscriptions/plan_create.html``
    (developer-facing; create subscription plan)
  * ``templates/subscriptions/plan_update.html``
    (developer-facing; update subscription plan)
  * ``templates/subscriptions/plan_delete.html``
    (developer-facing; delete subscription plan)
  * ``templates/subscriptions/plan_list_list.html``
    (developer-facing; list of all plan lists)
  * ``templates/subscriptions/plan_list_create.html``
    (developer-facing; create new plan list)
  * ``templates/subscriptions/plan_list_update.html``
    (developer-facing; update plan list)
  * ``templates/subscriptions/plan_list_delete.html``
    (developer-facing; delete plan list)
  * ``templates/subscriptions/plan_list_detail_list.html``
    (developer-facing; list of plan list details)
  * ``templates/subscriptions/plan_list_detail_create.html``
    (developer-facing; create new plan list detail)
  * ``templates/subscriptions/plan_list_detail_update.html``
    (developer-facing; update plan list detail)
  * ``templates/subscriptions/plan_list_detail_delete.html``
    (developer-facing; delete plan list detail)
  * ``templates/subscriptions/subscription_list.html``
    (developer-facing; list all user's subscription plans)
  * ``templates/subscriptions/subscription_create.html``
    (developer-facing; create new subscription plan for user)
  * ``templates/subscriptions/subscription_update.html``
    (developer-facing; update subscription plan for user)
  * ``templates/subscriptions/subscription_delete.html``
    (developer-facing; delete subscription plan for user)
  * ``templates/subscriptions/tag_list.html``
    (developer-facing; list of tags)
  * ``templates/subscriptions/tag_create.html``
    (developer-facing; create new tag)
  * ``templates/subscriptions/tag_update.html``
    (developer-facing; update tag)
  * ``templates/subscriptions/tag_delete.html``
    (developer-facing; delete tag)
  * ``templates/subscriptions/transaction_list.html``
    (developer-facing; list of transactions)
  * ``templates/subscriptions/tag_detail.html``
    (developer-facing; details of a single transaction)

-----------------
Adding a currency
-----------------

Currently currencies are controlled by the ``CURRENCY`` dictionary in
the ``conf.py`` file. New currencies can be added by making a pull
request with the desired details. A future update will allow specifying
currencies in the settings file.

-------------------------------------
Customizing new subscription handling
-------------------------------------

All subscriptions are handled via the ``SubscribeView``. It is expected
that most applications will will extend this view to implement some
custom handling (e.g. payment processing). To extend this view:

1. Create a new view file (e.g. ``/custom/views.py``) and extend the
   ``Subscribe View``

.. code-block:: python

    # /custom/views.py
    from subscriptions import views

    class CustomSubscriptionView(views.SubscriptionView):
        pass

2. Update your settings file to point to the new view:

.. code-block:: python

    DFS_SUBSCRIBE_VIEW = custom.views.CustomSubscriptionView

From here you can override any attributes or methods to implement
custom handling. A list of all attributes and methods can be found
in the :doc:`package reference</subscriptions>`.

Adding payment processing
=========================

To implement payment processing, you will likely want to override
the ``process_payment`` method in ``SubscribeView`` (see
`Customizing new subscription handling`_. This method is called when a
user confirms payment. The request must pass validation of form
specified in the ``payment_form`` attribute (defaults to
``PaymentForm``).

You may also need to implement a custom ``PaymentForm`` if you require
different fields or validation than the default provided in
``django-flexible-subscriptions``. You can do this by creating a new
form and assigning it as value for the ``payment_form`` attribute of a
custom ``SubscribeView``:

1. Create a new view file (e.g. ``/custom/forms.py``) and create a
   a Django form or extend the ``django-flexible-subscriptions``
   ``PaymentForm``:

.. code-block:: python

    # /custom/forms.py
    from subscriptions.forms import PaymentForm

    class CustomPaymentForm(PaymentForm):
        pass

2. Update your custom ``SubscribeView`` to point to your new form:

.. code-block:: python

    # custom/views.py
    from custom.forms import CustomPaymentForm

    class CustomSubscriptionView(views.SubscriptionView):
        payment_form = CustomPaymentForm

----------------------------------
Subscription renewals and expiries
----------------------------------

TBD
