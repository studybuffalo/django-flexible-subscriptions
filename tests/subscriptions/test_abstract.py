"""Tests for the abstract module."""
from unittest.mock import patch

from subscriptions import abstract


def test_template_view_get_context_data():
    """Tests that context is properly extended."""
    view = abstract.TemplateView()
    context = view.get_context_data()

    assert 'template_extends' in context
    assert context['template_extends'] == 'subscriptions/base.html'


def test_list_view_get_context_data():
    """Tests that context is properly extended."""
    view = abstract.ListView()
    view.object = None
    view.object_list = None
    context = view.get_context_data()

    assert 'template_extends' in context
    assert context['template_extends'] == 'subscriptions/base.html'


def test_detail_view_get_context_data():
    """Tests that context is properly extended."""
    view = abstract.DetailView()
    view.object = None
    context = view.get_context_data()

    assert 'template_extends' in context
    assert context['template_extends'] == 'subscriptions/base.html'


@patch('subscriptions.abstract.CreateView.get_queryset', lambda x: True)
@patch('subscriptions.abstract.CreateView.get_form_class', lambda x: True)
@patch('subscriptions.abstract.CreateView.get_form_kwargs', lambda x: True)
@patch('subscriptions.abstract.CreateView.get_form', lambda x: True)
def test_create_view_get_context_data():
    """Tests that context is properly extended."""
    view = abstract.CreateView()
    view.object = None
    context = view.get_context_data()

    assert 'template_extends' in context
    assert context['template_extends'] == 'subscriptions/base.html'


@patch('subscriptions.abstract.UpdateView.get_queryset', lambda x: True)
@patch('subscriptions.abstract.UpdateView.get_form_class', lambda x: True)
@patch('subscriptions.abstract.UpdateView.get_form_kwargs', lambda x: True)
@patch('subscriptions.abstract.UpdateView.get_form', lambda x: True)
def test_update_view_get_context_data():
    """Tests that context is properly extended."""
    view = abstract.UpdateView()
    view.object = None
    context = view.get_context_data()

    assert 'template_extends' in context
    assert context['template_extends'] == 'subscriptions/base.html'


def test_delete_view_get_context_data():
    """Tests that context is properly extended."""
    view = abstract.DeleteView()
    view.object = None
    context = view.get_context_data()

    assert 'template_extends' in context
    assert context['template_extends'] == 'subscriptions/base.html'
