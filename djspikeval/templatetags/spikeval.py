# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django import template
from django.apps import apps
from django.conf import settings
from django.shortcuts import resolve_url
from django.template.defaultfilters import slugify

from ..util import get_pc


User = apps.get_registered_model(*settings.AUTH_USER_MODEL.split("."))
Benchmark = apps.get_registered_model("djspikeval", "benchmark")
# Module = apps.get_registered_model("spike", "module")
register = template.Library()

## FILTER

@register.filter
def ident(obj):
    """returns ident slug for use in templates

    :param obj: django model instance
    :type obj:
    :return: slugified ident str
    """

    return slugify("%s-%s" % (obj.__class__.__name__, obj.pk))


@register.filter
def cls_name(obj):
    try:
        return obj.__class__.__name__
    except:
        return "&lt;unknown&gt;"


@register.filter
def is_editable(obj, user):
    if user.is_superuser:
        return True
    if hasattr(obj, "is_editable"):
        return obj.is_editable(user)
    if hasattr(obj, "owner"):
        return obj.owner == user
    else:
        return None


@register.filter
def in_group(user, groups):
    """Returns a boolean if the user is in the given group, or comma-separated
    list of groups.

    Usage::

        {% if user|in_group:"Friends" %}
        ...
        {% endif %}

    or::

        {% if user|in_group:"Friends,Enemies" %}
        ...
        {% endif %}

    """

    rval = False
    try:
        group_list = groups.split(",")
        rval = bool(user.groups.filter(name__in=group_list).values("name"))
    except:
        pass
    finally:
        return rval


@register.filter
def populate(form, instance):
    """populate a model form with an instance"""

    rval = form
    try:
        form = form.__class__(instance=instance)
    except:
        pass
    finally:
        return form


## TAGS

@register.simple_tag
def state_color(value):
    try:
        ival = int(value)
        if ival >= 0 and ival < 10:
            # in progress
            return "color: red"
        elif ival >= 10 and ival < 20:
            # failure
            return "color: blue"
        elif ival >= 20:
            # success
            return "color: green"
    except:
        return value


@register.simple_tag
def plot_color(value):
    try:
        ival = int(value)
        return get_pc(ival)
    except:
        return "#000000"


@register.simple_tag
def zero_red(value):
    try:
        ival = int(value)
        if ival == 0:
            return "color: red"
        else:
            return "color: green"
    except:
        return value


@register.simple_tag
def clear_search_url(request):
    getvars = request.GET.copy()
    if "search" in getvars:
        del getvars["search"]
    if len(getvars.keys()) > 0:
        return "%s?%s" % (request.path, getvars.urlencode())
    else:
        return request.path


@register.inclusion_tag("djspikeval/_delete_old.html")
def delete(obj, btn_name="delete", delete_url=None):
    """deletes the object"""

    if delete_url is None:
        delete_url = getattr(obj, "get_delete_url", ("delete_url", "#"))
    disabled = delete_url == "#"

    return {
        "obj": obj,
        "btn_name": btn_name,
        "delete_url": delete_url,
        "disabled": disabled}


@register.inclusion_tag("djspikeval/_attachments.html", takes_context=True)
def appendix(context, obj):
    """appendix for object"""

    return {"obj": obj,
            "appendix": obj.datafile_set.filter(kind="appendix"),
            "user": context['user']}


@register.inclusion_tag("djspikeval/_action.html")
def action(name, **kwargs):
    """render action button"""

    icon = kwargs.pop("icon", None)
    href = kwargs.pop("href", None)
    if href is not None:
        href = resolve_url(href, **kwargs)

    return {"name": name,
            "icon": icon,
            "href": href}


if __name__ == "__main__":
    pass
