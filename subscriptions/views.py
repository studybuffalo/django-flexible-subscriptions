"""Views for the Flexible Subscriptions app."""
from copy import copy

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin
)
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import HiddenInput
from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect
from django.http.response import HttpResponseNotAllowed, HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.utils import timezone

from subscriptions import models, forms, abstract


# Dashboard View
# -----------------------------------------------------------------------------
class DashboardView(PermissionRequiredMixin, abstract.TemplateView):
    """Dashboard view to manage subscription details."""
    permission_required = 'subscriptions.subscriptions'
    raise_exception = True
    template_name = 'subscriptions/dashboard.html'

# Tag Views
# -----------------------------------------------------------------------------
class TagListView(PermissionRequiredMixin, abstract.ListView):
    """List of all tags."""
    model = models.PlanTag
    permission_required = 'subscriptions.subscriptions'
    raise_exception = True
    context_object_name = 'tags'
    template_name = 'subscriptions/tag_list.html'

class TagCreateView(
        PermissionRequiredMixin, SuccessMessageMixin, abstract.CreateView
):
    """View to create a new tag."""
    model = models.PlanTag
    permission_required = 'subscriptions.subscriptions'
    raise_exception = True
    context_object_name = 'tag'
    fields = ['tag']
    success_message = 'Tag successfully added'
    success_url = reverse_lazy('dfs_tag_list')
    template_name = 'subscriptions/tag_create.html'

class TagUpdateView(
        PermissionRequiredMixin, SuccessMessageMixin, abstract.UpdateView
):
    """View to update the details of a tag."""
    model = models.PlanTag
    permission_required = 'subscriptions.subscriptions'
    raise_exception = True
    context_object_name = 'tag'
    fields = ['tag']
    success_message = 'Tag successfully updated'
    success_url = reverse_lazy('dfs_tag_list')
    pk_url_kwarg = 'tag_id'
    template_name = 'subscriptions/tag_update.html'

class TagDeleteView(PermissionRequiredMixin, abstract.DeleteView):
    """View to delete a tag.

        View is extended to handle additional attributes noted below.

        Attributes:
            success_message (str): Message to display on successful deletion.
            success_url (str): URL to redirect to on successful deletion.
    """
    model = models.PlanTag
    permission_required = 'subscriptions.subscriptions'
    raise_exception = True
    context_object_name = 'tag'
    pk_url_kwarg = 'tag_id'
    success_message = 'Tag successfully deleted'
    success_url = reverse_lazy('dfs_tag_list')
    template_name = 'subscriptions/tag_delete.html'

    def delete(self, request, *args, **kwargs):
        """Override delete to allow success message to be added."""
        messages.success(self.request, self.success_message)
        return super(TagDeleteView, self).delete(request, *args, **kwargs)


# Subscription Plan Views
# -----------------------------------------------------------------------------
class PlanListView(PermissionRequiredMixin, abstract.ListView):
    """List of all subscription plans."""
    model = models.SubscriptionPlan
    permission_required = 'subscriptions.subscriptions'
    raise_exception = True
    context_object_name = 'plans'
    template_name = 'subscriptions/plan_list.html'

class PlanCreateView(PermissionRequiredMixin, abstract.CreateView):
    """View to create a new subscription plan.

        View is extended to handle additional attributes noted below.

        Attributes:
            success_message (str): Message to display on successful creation.
            success_url (str): URL to redirect to on successful creation.
    """
    # pylint: disable=arguments-differ, attribute-defined-outside-init
    model = models.SubscriptionPlan
    permission_required = 'subscriptions.subscriptions'
    raise_exception = True
    context_object_name = 'plan'
    form_class = forms.SubscriptionPlanForm
    success_message = 'Subscription plan successfully added'
    success_url = reverse_lazy('dfs_plan_list')
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
        """Handles processing of valid forms.

            Parameters:
                form (obj): Parent SubscriptionPlanForm instance to
                    process.
                cost_forms (obj): PlanCostFormSet instance to process.

            Returns:
                obj: HttpResponseRedirect object to ``success_url``.
        """
        # Save the models
        self.object = form.save()
        cost_forms.instance = self.object
        cost_forms.save()

        # Generate the success message
        messages.success(self.request, self.success_message)

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, cost_forms):
        """Handles re-rendering invalid forms with errors.

            Parameters:
                form (obj): Parent SubscriptionPlanForm instance to
                    return.
                cost_forms (obj): PlanCostFormSet instance to return.

            Returns:
                obj: Renders original page with form content."""
        return self.render_to_response(
            self.get_context_data(
                form=form,
                cost_forms=cost_forms,
            )
        )

class PlanUpdateView(PermissionRequiredMixin, abstract.UpdateView):
    """View to update a subscription plan.

        View is extended to handle additional attributes noted below.

        Attributes:
            success_message (str): Message to display on successful creation.
            success_url (str): URL to redirect to on successful creation.

    """
    # pylint: disable=arguments-differ, attribute-defined-outside-init
    model = models.SubscriptionPlan
    permission_required = 'subscriptions.subscriptions'
    raise_exception = True
    context_object_name = 'plan'
    form_class = forms.SubscriptionPlanForm
    pk_url_kwarg = 'plan_id'
    success_message = 'Subscription plan successfully updated'
    success_url = reverse_lazy('dfs_plan_list')
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
        """Handles processing of valid forms.

            Parameters:
                form (obj): Parent SubscriptionPlanForm instance to
                    process.
                cost_forms (obj): PlanCostFormSet instance to process.

            Returns:
                obj: HttpResponseRedirect object to ``success_url``.
        """
        # Save the models
        self.object = form.save()
        cost_forms.instance = self.object
        cost_forms.save()

        # Generate the success message
        messages.success(self.request, self.success_message)

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, cost_forms):
        """Handles re-rendering invalid forms with errors.

            Parameters:
                form (obj): Parent SubscriptionPlanForm instance to
                    return.
                cost_forms (obj): PlanCostFormSet instance to return.

            Returns:
                obj: Renders original page with form content."""
        return self.render_to_response(
            self.get_context_data(
                form=form,
                cost_forms=cost_forms,
            )
        )

class PlanDeleteView(PermissionRequiredMixin, abstract.DeleteView):
    """View to delete a subscription plan.

        View is extended to handle additional attributes noted below.

        Attributes:
            success_message (str): Message to display on successful creation.
            success_url (str): URL to redirect to on successful creation.
    """
    model = models.SubscriptionPlan
    permission_required = 'subscriptions.subscriptions'
    raise_exception = True
    context_object_name = 'plan'
    pk_url_kwarg = 'plan_id'
    success_message = 'Subscription plan successfully deleted'
    success_url = reverse_lazy('dfs_plan_list')
    template_name = 'subscriptions/plan_delete.html'

    def delete(self, request, *args, **kwargs):
        """Override delete to allow success message to be added."""
        messages.success(self.request, self.success_message)
        return super(PlanDeleteView, self).delete(request, *args, **kwargs)


# User Subscription Views
# -----------------------------------------------------------------------------.
class SubscriptionListView(PermissionRequiredMixin, abstract.ListView):
    """List of all subscriptions for the users"""
    model = get_user_model()
    permission_required = 'subscriptions.subscriptions'
    raise_exception = True
    context_object_name = 'users'
    queryset = model.objects.all().exclude(subscriptions=None).order_by('username') # pylint: disable=line-too-long
    paginate_by = 100
    template_name = 'subscriptions/subscription_list.html'

class SubscriptionCreateView(
        PermissionRequiredMixin, SuccessMessageMixin, abstract.CreateView
):
    """View to create a new user subscription."""
    model = models.UserSubscription
    permission_required = 'subscriptions.subscriptions'
    raise_exception = True
    context_object_name = 'subscription'
    fields = ['user', 'subscription', 'date_billing_start', 'date_billing_end']
    success_message = 'User subscription successfully added'
    success_url = reverse_lazy('dfs_subscription_list')
    template_name = 'subscriptions/subscription_create.html'

class SubscriptionUpdateView(
        PermissionRequiredMixin, SuccessMessageMixin, abstract.UpdateView
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
    success_url = reverse_lazy('dfs_subscription_list')
    template_name = 'subscriptions/subscription_update.html'

class SubscriptionDeleteView(PermissionRequiredMixin, abstract.DeleteView):
    """View to delete a user subscription.

        View is extended to handle additional attributes noted below.

        Attributes:
            success_message (str): Message to display on successful creation.
            success_url (str): URL to redirect to on successful creation.
    """
    model = models.UserSubscription
    permission_required = 'subscriptions.subscriptions'
    raise_exception = True
    context_object_name = 'subscription'
    pk_url_kwarg = 'subscription_id'
    success_message = 'User subscription successfully deleted'
    success_url = reverse_lazy('dfs_subscription_list')
    template_name = 'subscriptions/subscription_delete.html'

    def delete(self, request, *args, **kwargs):
        """Override delete to allow success message to be added."""
        messages.success(self.request, self.success_message)
        return super(SubscriptionDeleteView, self).delete(
            request, *args, **kwargs
        )


# Subscription Transaction Views
# -----------------------------------------------------------------------------
class TransactionListView(PermissionRequiredMixin, abstract.ListView):
    """List of all subscription payment transactions."""
    model = models.SubscriptionTransaction
    permission_required = 'subscriptions.subscriptions'
    raise_exception = True
    context_object_name = 'transactions'
    paginate_by = 50
    template_name = 'subscriptions/transaction_list.html'

class TransactionDetailView(PermissionRequiredMixin, abstract.DetailView):
    """Shows details of a specific subscription payment transaction."""
    model = models.SubscriptionTransaction
    permission_required = 'subscriptions.subscriptions'
    raise_exception = True
    context_object_name = 'transaction'
    pk_url_kwarg = 'transaction_id'
    template_name = 'subscriptions/transaction_detail.html'


# PlanList Views
# -----------------------------------------------------------------------------
class PlanListListView(PermissionRequiredMixin, abstract.ListView):
    """List of plan lists."""
    model = models.PlanList
    permission_required = 'subscriptions.subscriptions'
    raise_exception = True
    context_object_name = 'plan_lists'
    template_name = 'subscriptions/plan_list_list.html'

class PlanListCreateView(
        PermissionRequiredMixin, SuccessMessageMixin, abstract.CreateView
):
    """View to create a new plan list."""
    model = models.PlanList
    permission_required = 'subscriptions.subscriptions'
    raise_exception = True
    context_object_name = 'plan_list'
    fields = ['title', 'subtitle', 'header', 'footer', 'active']
    success_message = 'Plan list successfully added'
    success_url = reverse_lazy('dfs_plan_list_list')
    template_name = 'subscriptions/plan_list_create.html'

class PlanListUpdateView(
        PermissionRequiredMixin, SuccessMessageMixin, abstract.UpdateView
):
    """View to update the details of a plan list."""
    model = models.PlanList
    permission_required = 'subscriptions.subscriptions'
    raise_exception = True
    context_object_name = 'plan_list'
    fields = ['title', 'subtitle', 'header', 'footer', 'active']
    success_message = 'Plan list successfully updated'
    success_url = reverse_lazy('dfs_plan_list_list')
    pk_url_kwarg = 'plan_list_id'
    template_name = 'subscriptions/plan_list_update.html'

class PlanListDeleteView(PermissionRequiredMixin, abstract.DeleteView):
    """View to delete a plan list.

        View is extended to handle additional attributes noted below.

        Attributes:
            success_message (str): Message to display on successful deletion.
            success_url (str): URL to redirect to on successful deletion.
    """
    model = models.PlanList
    permission_required = 'subscriptions.subscriptions'
    raise_exception = True
    context_object_name = 'plan_list'
    pk_url_kwarg = 'plan_list_id'
    success_message = 'Plan list successfully deleted'
    success_url = reverse_lazy('dfs_plan_list_list')
    template_name = 'subscriptions/plan_list_delete.html'

    def delete(self, request, *args, **kwargs):
        """Override delete to allow success message to be added."""
        messages.success(self.request, self.success_message)
        return super(PlanListDeleteView, self).delete(request, *args, **kwargs)


# PlanListDetail Views
# -----------------------------------------------------------------------------
class PlanListDetailListView(PermissionRequiredMixin, abstract.DetailView):
    """List of plan lists."""
    model = models.PlanList
    pk_url_kwarg = 'plan_list_id'
    permission_required = 'subscriptions.subscriptions'
    raise_exception = True
    context_object_name = 'plan_list'
    template_name = 'subscriptions/plan_list_detail_list.html'

class PlanListDetailCreateView(
        PermissionRequiredMixin, SuccessMessageMixin, abstract.CreateView
):
    """View to create a new plan list."""
    model = models.PlanListDetail
    fields = [
        'plan', 'plan_list', 'html_content', 'subscribe_button_text', 'order'
    ]
    permission_required = 'subscriptions.subscriptions'
    raise_exception = True
    success_message = 'Subscription plan successfully added to plan list'
    template_name = 'subscriptions/plan_list_detail_create.html'

    def get_context_data(self, **kwargs):
        """Extend context to include the parent PlanList object."""
        context = super().get_context_data(**kwargs)

        context['plan_list'] = get_object_or_404(
            models.PlanList, id=self.kwargs.get('plan_list_id', None)
        )

        return context

    def get_success_url(self):
        return reverse_lazy(
            'dfs_plan_list_detail_list',
            kwargs={'plan_list_id': self.kwargs['plan_list_id']},
        )

class PlanListDetailUpdateView(
        PermissionRequiredMixin, SuccessMessageMixin, abstract.UpdateView
):
    """View to update the details of a plan list detail."""
    model = models.PlanListDetail
    permission_required = 'subscriptions.subscriptions'
    raise_exception = True
    fields = [
        'plan', 'plan_list', 'html_content', 'subscribe_button_text', 'order'
    ]
    success_message = 'Plan list details successfully updated'
    pk_url_kwarg = 'plan_list_detail_id'
    template_name = 'subscriptions/plan_list_detail_update.html'

    def get_context_data(self, **kwargs):
        """Extend context to include the parent PlanList object."""
        context = super().get_context_data(**kwargs)

        context['plan_list'] = get_object_or_404(
            models.PlanList, id=self.kwargs.get('plan_list_id', None)
        )

        return context

    def get_success_url(self):
        return reverse_lazy(
            'dfs_plan_list_detail_list',
            kwargs={'plan_list_id': self.kwargs['plan_list_id']},
        )

class PlanListDetailDeleteView(PermissionRequiredMixin, abstract.DeleteView):
    """View to delete a plan list detail.

        View is extended to handle additional attributes noted below.

        Attributes:
            success_message (str): Message to display on successful deletion.
            success_url (str): URL to redirect to on successful deletion.
    """
    model = models.PlanListDetail
    permission_required = 'subscriptions.subscriptions'
    raise_exception = True
    context_object_name = 'plan_list_detail'
    pk_url_kwarg = 'plan_list_detail_id'
    success_message = 'Subscription plan successfully removed from plan list'
    template_name = 'subscriptions/plan_list_detail_delete.html'

    def get_context_data(self, **kwargs):
        """Extend context to include the parent PlanList object."""
        context = super().get_context_data(**kwargs)

        context['plan_list'] = get_object_or_404(
            models.PlanList, id=self.kwargs.get('plan_list_id', None)
        )

        return context

    def delete(self, request, *args, **kwargs):
        """Override delete to allow success message to be added."""
        messages.success(self.request, self.success_message)
        return super(PlanListDetailDeleteView, self).delete(
            request, *args, **kwargs
        )

    def get_success_url(self):
        return reverse_lazy(
            'dfs_plan_list_detail_list',
            kwargs={'plan_list_id': self.kwargs['plan_list_id']},
        )


# Subscribe Views
# -----------------------------------------------------------------------------
class SubscribeList(abstract.TemplateView):
    """Detail view of the first active PlanList instance.

        View is designed to be the user-facing subscription list and
        customizable through the PlanList and PlanListDetail models.
    """
    context_object_name = 'plan_list'
    template_name = 'subscriptions/subscribe_list.html'

    def get(self, request, *args, **kwargs):
        """Ensures content is available to display, then returns page."""
        # Get the appropriate plan list
        plan_list = models.PlanList.objects.filter(active=True).first()

        # Retrieve the plan details for template display
        details = models.PlanListDetail.objects.filter(
            plan_list=plan_list, plan__costs__isnull=False
        ).order_by('order')

        if plan_list:
            response = TemplateResponse(
                request,
                self.template_name,
                self.get_context_data(plan_list=plan_list, details=details)
            )

            return response

        return HttpResponseNotFound('No subscription plans are available')

    def get_context_data(self, **kwargs):
        """Extend context to include the parent PlanList object."""
        context = super().get_context_data(**kwargs)

        context['plan_list'] = kwargs['plan_list']
        context['details'] = kwargs['details']

        return context

class SubscribeView(LoginRequiredMixin, abstract.TemplateView):
    """View to handle all aspects of the subscribing process.

        This view will need to be subclassed and some methods
        overridden to implement the payment solution.

        Additionally, this view is extended from a TemplateView with
        the additional attributes noted below.

        Attributes:
            payment_form (obj): Django Form to handle subscription
                payment.
            subscription_plan (obj): A SubscriptionPlan instance. Will
                be set by methods during processing.
            success_url (str): URL to redirect to on successful
                creation.
            template_preview (str): Path to HTML template for the
                preview view.
            template_confirmation (str): Path to HTML template for the
                confirmation view.

        Notes:
            View only accessible via POST requests. The request must
            include an ID to a SubscriptionPlan +/- associated PlanCost
            instance (if past the preview view).
    """
    confirmation = False
    payment_form = forms.PaymentForm
    subscription_plan = None
    success_url = 'dfs_subscribe_thank_you'
    template_preview = 'subscriptions/subscribe_preview.html'
    template_confirmation = 'subscriptions/subscribe_confirmation.html'

    def get_object(self):
        """Gets the subscription plan object."""
        return get_object_or_404(
            models.SubscriptionPlan, id=self.request.POST.get('plan_id', None)
        )

    def get_context_data(self, **kwargs):
        """Overriding get_context_data to add additional context."""
        context = super(SubscribeView, self).get_context_data(**kwargs)

        # Whether this is a preview or confirmation step
        context['confirmation'] = self.confirmation

        # The plan instance to use for generating plan details
        context['plan'] = self.subscription_plan

        return context

    def get_template_names(self):
        """Returns the proper template name based on payment stage."""
        conf_templates = [self.template_confirmation]
        prev_templates = [self.template_preview]

        return conf_templates if self.confirmation else prev_templates

    def get_success_url(self, **kwargs):
        """Returns the success URL."""
        return reverse_lazy(self.success_url, kwargs=kwargs)

    def get(self, request, *args, **kwargs):
        """Returns 404 error as this method is not implemented."""
        return HttpResponseNotAllowed(['POST'])

    def post(self, request, *args, **kwargs):
        """Handles all POST requests to the SubscribeView.

            The 'action' POST argument is used to determine which
            context to render.

            Notes:
                The ``action`` POST parameter determines what stage to
                progress view to. ``None`` directs to preview
                processing, ``confirm`` directs to confirmation
                processing, and ``process`` directs to payment and
                subscription processing.
        """
        # Get the subscription plan for this POST
        self.subscription_plan = self.get_object()

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
        if 'error' in kwargs:
            plan_cost_form = forms.SubscriptionPlanCostForm(
                request.POST, subscription_plan=self.subscription_plan
            )
            payment_form = self.payment_form(request.POST)
        else:
            plan_cost_form = forms.SubscriptionPlanCostForm(
                initial=request.POST, subscription_plan=self.subscription_plan
            )
            payment_form = self.payment_form(initial=request.POST)

        context['plan_cost_form'] = plan_cost_form
        context['payment_form'] = payment_form

        return self.render_to_response(context)

    def render_confirmation(self, request, **kwargs):
        """Renders a confirmation page before processing payment.

            If forms are invalid will return to preview view for user
            to correct errors.
        """
        # Retrive form details
        plan_cost_form = forms.SubscriptionPlanCostForm(
            request.POST, subscription_plan=self.subscription_plan
        )
        payment_form = self.payment_form(request.POST)

        # Validate form submission
        if all([payment_form.is_valid(), plan_cost_form.is_valid()]):
            self.confirmation = True
            context = self.get_context_data(**kwargs)

            # Forms to process payment (hidden to prevent editing)
            context['plan_cost_form'] = self.hide_form(plan_cost_form)
            context['payment_form'] = self.hide_form(payment_form)

            # Add the PlanCost instance to context for use in template
            context['plan_cost'] = plan_cost_form.cleaned_data['plan_cost']

            return self.render_to_response(context)

        # Invalid form submission - render preview again
        kwargs['error'] = True
        return self.render_preview(request, **kwargs)

    def process_subscription(self, request, **kwargs):
        """Moves forward with payment & subscription processing.

            If forms are invalid will move back to confirmation page
            for user to correct errors.
        """
        # Validate payment details again incase anything changed
        plan_cost_form = forms.SubscriptionPlanCostForm(
            request.POST, subscription_plan=self.subscription_plan
        )
        payment_form = self.payment_form(request.POST)

        if all([payment_form.is_valid(), plan_cost_form.is_valid()]):
            # Attempt to process payment
            payment_transaction = self.process_payment(
                payment_form=payment_form,
                plan_cost_form=plan_cost_form,
            )

            if payment_transaction:
                # Payment successful - can handle subscription processing
                subscription = self.setup_subscription(
                    request.user, plan_cost_form.cleaned_data['plan_cost']
                )

                # Record the transaction details
                transaction = self.record_transaction(
                    subscription,
                    self.retrieve_transaction_date(payment_transaction)
                )

                return HttpResponseRedirect(
                    self.get_success_url(transaction_id=transaction.id)
                )

            # Payment unsuccessful, add message for confirmation page
            messages.error(request, 'Error processing payment')

        # Invalid form submission/payment - render preview again
        return self.render_confirmation(request, **kwargs)

    def hide_form(self, form):
        """Replaces form widgets with hidden inputs.

            Parameters:
                form (obj): A form instance.

            Returns:
                obj: The modified form instance.
        """
        for _, field in form.fields.items():
            field.widget = HiddenInput()

        return form

    def process_payment(self, *args, **kwargs): # pylint: disable=unused-argument
        """Processes payment and confirms if payment is accepted.

            This method needs to be overriden in a project to handle
            payment processing with the appropriate payment provider.

            Can return value that evalutes to ``True`` to indicate
            payment success and any value that evalutes to ``False`` to
            indicate payment error.
        """
        return True

    def setup_subscription(self, request_user, plan_cost):
        """Adds subscription to user and adds them to required group.

            Parameters:
                request_user (obj): A Django user instance.
                plan_cost (obj): A PlanCost instance.

            Returns:
                obj: The newly created UserSubscription instance.
        """
        current_date = timezone.now()

        # Add subscription plan to user
        subscription = models.UserSubscription.objects.create(
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

        return subscription

    def retrieve_transaction_date(self, payment): # pylint: disable=unused-argument
        """Returns the transaction date from provided payment details.

            Method should be overriden to accomodate the implemented
            payment processing if a more accurate datetime is required.


            Returns
                obj: The current datetime.
        """
        return timezone.now()

    def record_transaction(self, subscription, transaction_date=None):
        """Records transaction details in SubscriptionTransaction.

            Parameters:
                subscription (obj): A UserSubscription object.
                transaction_date (obj): A DateTime object of when
                    payment occurred (defaults to current datetime if
                    none provided).

            Returns:
                obj: The created SubscriptionTransaction instance.
        """
        if transaction_date is None:
            transaction_date = timezone.now()

        return models.SubscriptionTransaction.objects.create(
            user=subscription.user,
            subscription=subscription.subscription,
            date_transaction=transaction_date,
            amount=subscription.subscription.cost,
        )

class SubscribeUserList(LoginRequiredMixin, abstract.ListView):
    """List of all a user's subscriptions."""
    model = models.UserSubscription
    context_object_name = 'subscriptions'
    template_name = 'subscriptions/subscribe_user_list.html'

    def get_queryset(self):
        """Overrides get_queryset to restrict list to logged in user."""
        return self.model.objects.filter(user=self.request.user, active=True)

class SubscribeThankYouView(LoginRequiredMixin, abstract.TemplateView):
    """A thank you page and summary for a new subscription."""
    template_name = 'subscriptions/subscribe_thank_you.html'
    context_object_name = 'transaction'

    def get_object(self):
        """Returns the provided transaction instance."""
        try:
            return models.SubscriptionTransaction.objects.get(
                id=self.kwargs['transaction_id'],
                user=self.request.user,
            )
        except models.SubscriptionTransaction.DoesNotExist:
            return None

    def get_context_data(self, **kwargs):
        """Overriding get_context_data to add additional context."""
        context = super(SubscribeThankYouView, self).get_context_data(**kwargs)

        # Adds the context object
        context[self.context_object_name] = self.get_object()

        return context

class SubscribeCancelView(LoginRequiredMixin, abstract.DetailView):
    """View to handle cancelling of subscription.

        View is extended to handle additional attributes noted below.

        Attributes:
            success_message (str): Message to display on successful creation.
            success_url (str): URL to redirect to on successful creation.
    """
    model = models.UserSubscription
    context_object_name = 'subscription'
    pk_url_kwarg = 'subscription_id'
    success_message = 'Subscription successfully cancelled'
    success_url = 'dfs_subscribe_user_list'
    template_name = 'subscriptions/subscribe_cancel.html'

    def get_object(self, queryset=None):
        """Overrides get_object to restrict to logged in user."""
        return get_object_or_404(
            self.model,
            user=self.request.user,
            id=self.kwargs['subscription_id'],
        )

    def get_success_url(self):
        """Returns the success URL."""
        return reverse_lazy(self.success_url)

    def post(self, request, *args, **kwargs):
        """Updates a subscription's details to cancel it."""
        subscription = self.get_object()
        subscription.date_billing_end = copy(subscription.date_billing_next)
        subscription.date_billing_next = None
        subscription.cancelled = True
        subscription.save()

        messages.success(self.request, self.success_message)

        return HttpResponseRedirect(self.get_success_url())
