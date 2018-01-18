from django.core.exceptions import PermissionDenied
from django.urls import reverse, exceptions
from django.utils import six

from .searchproviders import searchproviders


def search_providers(request):
    allowed_providers = []

    try:
        if request.user.acl_cache['can_search']:
            allowed_providers = searchproviders.get_allowed_providers(request)
    except AttributeError:
        # is user has no acl_cache attribute, cease entire middleware
        # this is edge case that occurs when debug toolbar intercepts
        # the redirect response from logout page and runs context providers
        # with non-misago's anonymous user model that has no acl support
        return {}

    request.frontend_context['SEARCH_URL'] = reverse('misago:search')
    request.frontend_context['SEARCH_API'] = reverse('misago:api:search')
    # TODO `search_autocomplete` feature is currently only implemented in
    # downstream repository, make it optional in Misago for now
    try:
        request.frontend_context['SEARCH_AUTOCOMPLETE_API'] = \
            reverse('search_autocomplete')
    except exceptions.NoReverseMatch:
        pass
    request.frontend_context['SEARCH_PROVIDERS'] = []

    for provider in allowed_providers:
        request.frontend_context['SEARCH_PROVIDERS'].append({
            'id': provider.url,
            'name': six.text_type(provider.name),
            'icon': provider.icon,
            'url': reverse('misago:search', kwargs={'search_provider': provider.url}),
            'api': reverse('misago:api:search', kwargs={'search_provider': provider.url}),
            'results': None,
            'time': None,
        })

    return {}
