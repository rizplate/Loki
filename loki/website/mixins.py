from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from .services import get_snippets


class SnippetBasedView:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['snippets'] = get_snippets()

        return context


class AnonymousRequired:
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return redirect(reverse('website:profile'))

        return super().dispatch(*args, **kwargs)
