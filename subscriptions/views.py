"""Views for the Flexible Subscriptions app."""
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import HiddenInput
from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect
from django.http.response import HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.views import generic
from django.urls import reverse_lazy
from django.utils import timezone

from subscriptions import models, forms

# TODO: Extend views to include a setting to specify the base template

# Tag Views
# -----------------------------------------------------------------------------
class TagListView(PermissionRequiredMixin, generic.ListView):
    """List of all tags."""
    model = models.PlanTag
    permission_required = 'subscriptions.subscriptions'
    raise_exception = True
    context_object_name = 'tags'
    template_name = 'subscriptions/tag_list.html'

class TagCreateView(
        PermissionRequiredMixin, SuccessMessageMixin, generic.CreateView
):
    """View to create a new tag."""
    model = models.PlanTag
    permission_required = 'subscriptions.subscriptions'
    raise_exception = True
    context_object_name = 'tag'
    fields = ['tag']
    success_message = 'Tag successfully added'
    success_url = reverse_lazy('subscriptions_tag_list')
    template_name = 'subscriptions/tag_create.html'

class TagUpdateView(
        PermissionRequiredMixin, SuccessMessageMixin, generic.UpdateView
):
    """View to update the details of a tag."""
    model = models.PlanTag
    permission_required = 'subscriptions.subscriptions'
    raise_exception = True
    context_object_name = 'tag'
    fields = ['tag']
    success_message = 'Tag successfully updated'
    success_url = reverse_lazy('subscriptions_tag_list')
    pk_url_kwarg = 'tag_id'
    template_name = 'subscriptions/tag_update.html'

class TagDeleteView(PermissionRequiredMixin, generic.DeleteView):
    """View to delete a tag."""
    model = models.PlanTag
    permission_required = 'subscriptions.subscriptions'
    raise_exception = True
    context_object_name = 'tag'
    pk_url_kwarg = 'tag_id'
    success_message = 'Tag successfully deleted'
    success_url = reverse_lazy('subscriptions_tag_list')
    template_name = 'subscriptions/tag_delete.html'

    def delete(self, request, *args, **kwargs):
        """Override delete to allow success message to be added."""
        messages.success(self.request, self.success_message)
        return super(TagDeleteView, self).delete(request, *args, **kwargs)


# Plan Views
# -----------------------------------------------------------------------------
class PlanListView(PermissionRequiredMixin, generic.ListView):
    """List of all subscription plans"""
    model = models.SubscriptionPlan
    permission_required = 'subscriptions.subscriptions'
    raise_exception = True
    context_object_name = 'plans'
    template_name = 'subscriptions/plan_list.html'

class PlanCreateView(PermissionRequiredMixin, generic.CreateView):
    """View to create a new subscription plan"""
    # pylint: disable=arguments-differ, attribute-defined-outside-init
    model = models.SubscriptionPlan
    permission_required = 'subscriptions.subscriptions'
    raise_exception = True
    context_object_name = 'plan'
    form_class = forms.SubscriptionPlanForm
    success_message = 'Subscription plan successfully added'
    success_url = reverse_lazy('subscriptions_plan_list')
    template_name = 'subscriptions/plan_create.html'

    def get(self, request, *args, **kwargs):
        """Overriding get method to handle inline formset."""
        # Setup the formset for PlanCost
        PlanCostFormSet = inlineformset_factory( # pylint: disable=invalid-name
            parent_model=models.SubscriptionPlan,
            model=models.PlanCost,
            form=forms.PlanCostForm,
            can_delete=False,
            extra=1,
        )

        self.object = None
        form = self.get_form(self.get_form_class())
        cost_forms = PlanCostFormSet()

        return self.render_to_response(
            self.get_context_data(
                form=form,
                cost_forms=cost_forms,
            )
        )

    def post(self, request, *args, **kwargs):
        """Overriding post method to handle inline formsets."""
        # Setup the formset for PlanCost
        PlanCostFormSet = inlineformset_factory( # pylint: disable=invalid-name
            parent_model=models.SubscriptionPlan,
            model=models.PlanCost,
            form=forms.PlanCostForm,
            can_delete=False,
            extra=1,
        )

        self.object = None
        form = self.get_form(self.get_form_class())
        cost_forms = PlanCostFormSet(self.request.POST)

        if form.is_valid() and cost_forms.is_valid():
            return self.form_valid(form, cost_forms)
        else:
            return self.form_invalid(form, cost_forms)

    def form_valid(self, form, cost_forms):
        """Handles processing of valid forms."""
        # Save the models
        self.object = form.save()
        cost_forms.instance = self.object
        cost_forms.save()

        # Generate the success message
        messages.success(self.request, self.success_message)

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, cost_forms):
        """Handles re-rendering invalid forms with errors."""
        return self.render_to_response(
            self.get_context_data(
                form=form,
                cost_forms=cost_forms,
            )
        )

class PlanUpdateView(PermissionRequiredMixin, generic.UpdateView):
    """View to update a subscription plan"""
    # pylint: disable=arguments-differ, attribute-defined-outside-init
    model = models.SubscriptionPlan
    permission_required = 'subscriptions.subscriptions'
    raise_exception = True
    context_object_name = 'plan'
    form_class = forms.SubscriptionPlanForm
    pk_url_kwarg = 'plan_id'
    success_message = 'Subscription plan successfully updated'
    success_url = reverse_lazy('subscriptions_plan_list')
    template_name = 'subscriptions/plan_update.html'

    def get(self, request, *args, **kwargs):
        """Overriding get method to handle inline formset."""
        # Setup the formset for PlanCost
        PlanCostFormSet = inlineformset_factory( # pylint: disable=invalid-name
            parent_model=models.SubscriptionPlan,
            model=models.PlanCost,
            form=forms.PlanCostForm,
            can_delete=True,
            extra=1,
        )

        self.object = self.get_object()
        form = self.get_form(self.get_form_class())
        cost_forms = PlanCostFormSet(instance=self.object)

        return self.render_to_response(
            self.get_context_data(
                form=form,
                cost_forms=cost_forms,
            )
        )

    def post(self, request, *args, **kwargs):
        """Overriding post method to handle inline formsets."""
        # Setup the formset for PlanCost
        PlanCostFormSet = inlineformset_factory( # pylint: disable=invalid-name
            parent_model=models.SubscriptionPlan,
            model=models.PlanCost,
            form=forms.PlanCostForm,
            can_delete=True,
            extra=1,
        )

        self.object = self.get_object()
        form = self.get_form(self.get_form_class())
        cost_forms = PlanCostFormSet(self.request.POST, instance=self.object)

        if form.is_valid() and cost_forms.is_valid():
            return self.form_valid(form, cost_forms)
        else:
            return self.form_invalid(form, cost_forms)

    def form_valid(self, form, cost_forms):
        """Handles processing of valid forms."""
        # Save the models
        self.object = form.save()
        cost_forms.instance = self.object
        cost_forms.save()

        # Generate the success message
        messages.success(self.request, self.success_message)

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, cost_forms):
        """Handles re-rendering invalid forms with errors."""
        return self.render_to_response(
            self.get_context_data(
                form=form,
                cost_forms=cost_forms,
            )
        )

class PlanDeleteView(PermissionRequiredMixin, generic.DeleteView):
    """View to delete a subscription plan"""
    model = models.SubscriptionPlan
    permission_required = 'subscriptions.subscriptions'
    raise_exception = True
    context_object_name = 'plan'
    pk_url_kwarg = 'plan_id'
    success_message = 'Subscription plan successfully deleted'
    success_url = reverse_lazy('subscriptions_plan_list')
    template_name = 'subscriptions/plan_delete.html'

    def delete(self, request, *args, **kwargs):
        """Override delete to allow success message to be added."""
        messages.success(self.request, self.success_message)
        return super(PlanDeleteView, self).delete(request, *args, **kwargs)


# User Subscription Views
# -----------------------------------------------------------------------------.
class SubscriptionListView(PermissionRequiredMixin, generic.ListView):
    """List of all subscriptions for the users"""
    model = get_user_model()
    permission_required = 'subscriptions.subscriptions'
    raise_exception = True
    context_object_name = 'users'
    queryset = model.objects.all().exclude(subscriptions=None).order_by('username') # pylint: disable=line-too-long
    paginate_by = 100
    template_name = 'subscriptions/subscription_list.html'

class SubscriptionCreateView(
        PermissionRequiredMixin, SuccessMessageMixin, generic.CreateView
):
    """View to create a new user subscription."""
    model = models.UserSubscription
    permission_required = 'subscriptions.subscriptions'
    raise_exception = True
    context_object_name = 'subscription'
    fields = ['user', 'subscription', 'date_billing_start', 'date_billing_end']
    success_message = 'User subscription successfully added'
    success_url = reverse_lazy('subscriptions_subscription_list')
    template_name = 'subscriptions/subscription_create.html'

class SubscriptionUpdateView(
        PermissionRequiredMixin, SuccessMessageMixin, generic.UpdateView
):
    """View to update the details of a user subscription."""
    model = models.UserSubscription
    permission_required = 'subscriptions.subscriptions'
    raise_exception = True
    context_object_name = 'subscription'
    fields = [
        'subscription', 'date_billing_start', 'date_billing_end',
        'date_billing_last', 'date_billing_next', 'active', 'cancelled'
    ]
    pk_url_kwarg = 'subscription_id'
    success_message = 'User subscription successfully updated'
    success_url = reverse_lazy('subscriptions_subscription_list')
    template_name = 'subscriptions/subscription_update.html'

class SubscriptionDeleteView(PermissionRequiredMixin, generic.DeleteView):
    """View to delete a user subscription."""
    model = models.UserSubscription
    permission_required = 'subscriptions.subscriptions'
    raise_exception = True
    context_object_name = 'subscription'
    pk_url_kwarg = 'subscription_id'
    success_message = 'User subscription successfully deleted'
    success_url = reverse_lazy('subscriptions_subscription_list')
    template_name = 'subscriptions/subscription_delete.html'

    def delete(self, request, *args, **kwargs):
        """Override delete to allow success message to be added."""
        messages.success(self.request, self.success_message)
        return super(SubscriptionDeleteView, self).delete(
            request, *args, **kwargs
        )


# Subscription Transaction Views
# -----------------------------------------------------------------------------
class TransactionListView(PermissionRequiredMixin, generic.ListView):
    """List of all subscription payment transactions."""
    model = models.SubscriptionTransaction
    permission_required = 'subscriptions.subscriptions'
    raise_exception = True
    context_object_name = 'transactions'
    paginate_by = 100
    template_name = 'subscriptions/transaction_list.html'

class TransactionDetailView(PermissionRequiredMixin, generic.DetailView):
    """Shows details of a specific subscription payment transaction."""
    model = models.SubscriptionTransaction
    permission_required = 'subscriptions.subscriptions'
    raise_exception = True
    context_object_name = 'transaction'
    pk_url_kwarg = 'transaction_id'
    template_name = 'subscriptions/transaction_detail.html'


# Subscribe Views
# -----------------------------------------------------------------------------
class SubscribeView(generic.TemplateView):
    """View to handle all aspects of the subscribing process."""
    confirmation = False
    payment_form = forms.PaymentForm
    subscription_plan = None
    success_url = 'subscriptions_dashboard'
    template_extends = 'subscriptions/base.html'
    template_preview = 'subscriptions/subscribe_preview.html'
    template_confirmation = 'subscriptions/subscribe_confirmation.html'

    def get_object(self, request):
        """Gets the subscription plan object."""
        return get_object_or_404(
            models.SubscriptionPlan, id=request.POST.get('plan_id', None)
        )
    def get_context_data(self, **kwargs):
        """Overriding get_context_data to add additional context."""
        context = super(SubscribeView, self).get_context_data(**kwargs)

        # Provides the base template to extend from
        context['template_extends'] = self.template_extends

        # Whether this is a preview or confirmation step
        context['confirmation'] = self.confirmation

        # The plan instance to use for generating plan details
        context['plan'] = self.subscription_plan

        return context

    def get_template_names(self):
        conf_templates = [self.template_confirmation]
        prev_templates = [self.template_preview]

        return conf_templates if self.confirmation else prev_templates

    def get_success_url(self):
        """Returns the success URL."""
        return reverse_lazy(self.success_url)

    def post(self, request, *args, **kwargs):
        """Handles all POST requests to the SubscribeView.

            The 'action' POST argument is used to determine which
            context to render.
        """
        # Get the subscription plan for this POST
        self.subscription_plan = self.get_object(request)

        # Determine POST action and direct to proper function
        post_action = request.POST.get('action', None)

        if post_action == 'confirm':
            return self.render_confirmation(request)

        if post_action == 'process':
            return self.process_subscription(request)

        # No action - assumes payment details need to be collected
        return self.render_preview(request)

    def render_preview(self, request, **kwargs):
        """Renders preview of subscription and collect payment details."""
        self.confirmation = False
        context = self.get_context_data(**kwargs)

        # Forms to collect subscription details
        context['plan_cost_form'] = forms.SubscriptionPlanCostForm(
            subscription_plan=self.subscription_plan
        )
        context['payment_form'] = self.payment_form()

        return self.render_to_response(context)

    def render_confirmation(self, request, **kwargs):
        """Renders a confirmation page before processing payment."""
        # Retrive form details
        plan_cost_form = forms.SubscriptionPlanCostForm(
            request.POST, subscription_plan=self.subscription_plan
        )
        payment_form = self.payment_form(request.POST)

        # Validate form submission
        if payment_form.is_valid() and plan_cost_form.is_valid():
            self.confirmation = True
            context = self.get_context_data(**kwargs)

            # Forms to process payment (hidden to prevent editing)
            context['plan_cost_form'] = self.hide_form(plan_cost_form)
            context['payment_form'] = self.hide_form(payment_form)

            return self.render_to_response(context)

        # Invalid form submission - render preview again
        self.confirmation = False
        context = self.get_context_data(**kwargs)
        context['plan_cost_form'] = plan_cost_form
        context['payment_form'] = payment_form

        return self.render_to_response(context)

    def process_subscription(self, request, **kwargs):
        """Moves forward with payment & subscription processing."""
        # Validate payment details again incase anything changed
        plan_cost_form = forms.SubscriptionPlanCostForm(
            request.POST, subscription_plan=self.subscription_plan
        )
        payment_form = self.payment_form(request.POST)

        if payment_form.is_valid() and plan_cost_form.is_valid():
            # Attempt to process payment
            payment_success = self.process_payment(payment_form)

            if payment_success:
                # Payment successful - can handle subscription processing
                self.setup_subscription(
                    request.user, plan_cost_form.cleaned_data['plan_cost']
                )

                return HttpResponseRedirect(self.get_success_url())

            # Payment unsuccessful, add message for confirmation page
            messages.error(request, 'Error processing payment')

        # Invalid form submission/payment - render confirmation again
        self.confirmation = True
        context = self.get_context_data(**kwargs)
        context['plan_cost_form'] = self.hide_form(plan_cost_form)
        context['payment_form'] = self.hide_form(payment_form)

        return self.render_to_response(context)

    def hide_form(self, form):
        """Returns form with hidden input widgets."""
        for _, field in form.fields.items():
            field.widget = HiddenInput()

        return form

    def process_payment(self, payment_form): # pylint: disable=unused-argument
        """Processes payment and confirms if payment is accepted.

            This method needs to be overriden in a project to handle
            payment processing with the appropriate payment provider.

            Returns:
                bool: True if payment is successful, False if an error
                    has occurred.
        """
        return True

    def setup_subscription(self, request_user, plan_cost_id):
        """Adds subscription to user and adds them to required group."""
        plan_cost = models.PlanCost.objects.get(id=plan_cost_id)
        current_date = timezone.now()

        # Add subscription plan to user
        models.UserSubscription.objects.create(
            user=request_user,
            subscription=plan_cost,
            date_billing_start=current_date,
            date_billing_end=None,
            date_billing_last=current_date,
            date_billing_next=plan_cost.next_billing_datetime(current_date),
            active=True,
            cancelled=False,
        )

        # Add user to the proper group
        try:
            group = self.subscription_plan.group
            group.user_set.add(request_user)
        except AttributeError:
            # No group available to add user to
            pass

class ThankYouView(generic.DetailView):
    """A thank you page and summary for a new subscription."""
    object = None
    template_name = 'subscriptions/subscribe_thank_you.html'
    template_extends = 'subscriptions/base.html'
    context_object_name = 'transaction'

    def get_context_data(self, **kwargs):
        """Overriding get_context_data to add additional context."""
        context = super(ThankYouView, self).get_context_data(**kwargs)

        # Provides the base template to extend from
        context['template_extends'] = self.template_extends

        return context

    def get_object(self, queryset=None):
        """Returns the provided transaction instance."""
        transaction = get_object_or_404(
            models.SubscriptionTransaction,
            id=self.request.GET.get('transaction_id', None)
        )

        return transaction

class SubscribeCancelView(PermissionRequiredMixin, generic.DetailView):
    """View to handle cancelling of subscription."""
    model = models.SubscriptionTransaction
    context_object_name = 'subscription'
    pk_url_kwarg = 'subscription_id'
    permission_required = 'subscriptions.subscriptions'
    raise_exception = True
    success_message = 'Subscription successfully cancelled'
    success_url = reverse_lazy('subscriptions_subscription_list')
    template_extends = 'subscriptions/base.html'
    template_name = 'subscriptions/subscribe_cancel.html'

    def get_context_data(self, **kwargs):
        """Overriding get_context_data to add additional context."""
        context = super(SubscribeCancelView, self).get_context_data(**kwargs)

        # Provides the base template to extend from
        context['template_extends'] = self.template_extends

        return context

    def get_success_url(self):
        """Returns the success URL."""
        return reverse_lazy(self.success_url)

    def post(self, request, *args, **kwargs):
        """Updates a subscription's details to cancel it."""
        subscription = self.object
        subscription.date_billing_end = subscription.date_billing_next
        subscription.date_billing_next = None
        subscription.save()

        messages.success(self.request, self.success_message)

        return HttpResponseRedirect(self.get_success_url())
