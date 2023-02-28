from django.template.context import RequestContext


def get_field_from_context(context, field_type):
    if isinstance(context, RequestContext):
        context = context.flatten()
    for field in context.keys():
        if field not in ('user', 'request') and isinstance(context[field], field_type):
            return context[field]
    return
