"""Views for the Flexible Subscriptions app."""
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic
from django.urls import reverse_lazy

from subscriptions import models


class TagListView(PermissionRequiredMixin, generic.ListView):
    """List of all tags."""
    model = models.PlanTag
    permission_required = 'subscriptions.subscriptions_plans'
    raise_exception = True
    context_object_name = 'tags'
    template_name = 'subscriptions/tag_list.html'

class TagCreateView(
        PermissionRequiredMixin, SuccessMessageMixin, generic.CreateView
):
    """View to create a new tag."""
    model = models.PlanTag
    permission_required = 'subscriptions.subscriptions_plans'
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
    permission_required = 'subscriptions.subscriptions_plans'
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
    permission_required = 'subscriptions.subscriptions_plans'
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

# Create view and forms to handle creation & update of plans/tags
# to skip admin if needed

# Create view to display transactions
#   Will need pagination

# Create view to view subscriptions +/- modify?
