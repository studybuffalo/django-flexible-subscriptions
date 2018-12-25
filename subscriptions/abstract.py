"""Abstract templates for the Djanog Flexible Subscriptions app."""
from django.views import generic

from subscriptions.conf import SETTINGS

BASE_TEMPLATE = SETTINGS['base_template']

class TemplateView(generic.TemplateView):
    """Extends TemplateView to specify of extensible HTML template.

        Attributes:
            template_extends (str): Path to HTML template that this
                view extends.
    """
    template_extends = BASE_TEMPLATE

    def get_context_data(self, **kwargs):
        """Overriding get_context_data to add additional context."""
        context = super(TemplateView, self).get_context_data(**kwargs)

        # Provides the base template to extend from
        context['template_extends'] = self.template_extends

        return context

class ListView(generic.ListView):
    """Extends ListView to specify of extensible HTML template

        Attributes:
            template_extends (str): Path to HTML template that this
                view extends.
    """
    template_extends = BASE_TEMPLATE

    def get_context_data(self, *, object_list=None, **kwargs): # pylint: disable=unused-argument
        """Overriding get_context_data to add additional context."""
        context = super(ListView, self).get_context_data(**kwargs)

        # Provides the base template to extend from
        context['template_extends'] = self.template_extends

        return context

class DetailView(generic.DetailView):
    """Extends DetailView to specify of extensible HTML template

        Attributes:
            template_extends (str): Path to HTML template that this
                view extends.
    """
    template_extends = BASE_TEMPLATE

    def get_context_data(self, **kwargs):
        """Overriding get_context_data to add additional context."""
        context = super(DetailView, self).get_context_data(**kwargs)

        # Provides the base template to extend from
        context['template_extends'] = self.template_extends

        return context

class CreateView(generic.CreateView):
    """Extends CreateView to specify of extensible HTML template

        Attributes:
            template_extends (str): Path to HTML template that this
                view extends.
    """
    template_extends = BASE_TEMPLATE

    def get_context_data(self, **kwargs):
        """Overriding get_context_data to add additional context."""
        context = super(CreateView, self).get_context_data(**kwargs)

        # Provides the base template to extend from
        context['template_extends'] = self.template_extends

        return context

class UpdateView(generic.UpdateView):
    """Extends UpdateView to specify of extensible HTML template

        Attributes:
            template_extends (str): Path to HTML template that this
                view extends.
    """
    template_extends = BASE_TEMPLATE

    def get_context_data(self, **kwargs):
        """Overriding get_context_data to add additional context."""
        context = super(UpdateView, self).get_context_data(**kwargs)

        # Provides the base template to extend from
        context['template_extends'] = self.template_extends

        return context

class DeleteView(generic.DeleteView):
    """Extends DeleteView to specify of extensible HTML template

        Attributes:
            template_extends (str): Path to HTML template that this
                view extends.
    """
    template_extends = BASE_TEMPLATE

    def get_context_data(self, **kwargs):
        """Overriding get_context_data to add additional context."""
        context = super(DeleteView, self).get_context_data(**kwargs)

        # Provides the base template to extend from
        context['template_extends'] = self.template_extends

        return context
