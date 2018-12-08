"""Views for the Flexible Subscriptions app."""
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse_lazy

from subscriptions import models, forms


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
    fields = ['user', 'plan', 'date_billing_start', 'date_billing_end']
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
        'plan', 'date_billing_start', 'date_billing_end', 'date_billing_last',
        'date_billing_next', 'active', 'cancelled'
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
