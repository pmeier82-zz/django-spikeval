# -*- coding: utf-8 -*-

from django import template

register = template.Library()


@register.simple_tag
def fa_text(text, icons, link=None, color=None, strong=False):
    try:
        text = text.strip()
    except:
        text = "{}".format(text)
    icons = " ".join(["fa-" + icon for icon in icons.split(",")])
    rval = "<nobr><i class=\"fa {icons}\"></i> {a}{c}{s}{text}{s_}{c_}{a_}</nobr>"
    return rval.format(
        icons=icons,
        a="<a href=\"{}\" title=\"{}\">".format(link, text) if link is not None else "",
        c="<span style=\"color: {};\">".format(color) if color is not None else "",
        s="<strong>" if strong is True else "",
        text=text,
        s_="</strong>" if strong is True else "",
        c_="</span>" if color is not None else "",
        a_="</a>" if link is not None else ""
    )


if __name__ == "__main__":
    pass
