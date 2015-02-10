# -*- coding: utf-8 -*-

from captcha.fields import ReCaptchaField

__author__ = "pmeier82"


def form_with_captcha(orig_form):
    if hasattr(orig_form, "recaptcha"):
        raise ValueError("form already has a field with name \"recaptcha\"!")
    orig_form.__orig__init__ = orig_form.__init__

    def new_init(self, *args, **kwargs):
        self.__orig__init__(*args, **kwargs)
        self.fields["recaptcha"] = self.captcha

    orig_form.__init__ = new_init
    orig_form.captcha = ReCaptchaField()
    return orig_form


if __name__ == "__main__":
    pass
