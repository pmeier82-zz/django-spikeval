##---IMPORTS

from django import forms
from django.apps import apps

from util import form_with_captcha

__all__ = ["AttachmentForm"]
__author__ = "pmeier82"

Attachment = apps.get_registered_model("djspikeval", "attachment")


class AttachmentForm(forms.ModelForm):
    """`Attachment` model form"""

    # meta
    class Meta:
        model = Attachment
        fields = ("name", "data")

    # constructor
    def __init__(self, *args, **kwargs):
        self.obj = kwargs.pop("obj", None)
        super(AttachmentForm, self).__init__(*args, **kwargs)

    # interface
    def save(self, *args, **kwargs):
        self.instance.kind = "attachment"
        self.instance.content_object = self.obj
        return super(AttachmentForm, self).save(*args, **kwargs)


if __name__ == "__main__":
    pass
