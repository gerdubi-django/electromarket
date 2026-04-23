from django import template
from django.urls import reverse
from django.utils.translation import override

register = template.Library()


@register.simple_tag
def localized_url(request, language_code):
    # Build the current route URL in the target language while preserving query params.
    if not request:
        return "/"

    resolver_match = getattr(request, "resolver_match", None)
    if not resolver_match:
        return request.get_full_path()

    kwargs = resolver_match.kwargs or {}
    args = resolver_match.args or ()

    try:
        with override(language_code):
            translated_path = reverse(resolver_match.view_name, args=args, kwargs=kwargs)
    except Exception:
        path = request.path
        parts = [segment for segment in path.split("/") if segment]
        if parts and len(parts[0]) == 2:
            parts[0] = language_code
            translated_path = f"/{'/'.join(parts)}/"
        else:
            translated_path = f"/{language_code}{path if path.startswith('/') else f'/{path}'}"

    query_string = request.META.get("QUERY_STRING", "")
    if query_string:
        return f"{translated_path}?{query_string}"

    return translated_path
