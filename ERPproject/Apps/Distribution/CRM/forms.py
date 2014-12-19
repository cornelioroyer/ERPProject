__author__ = 'FARID ILHAM Al-Q'

from django import forms
from captcha.fields import CaptchaField

from Apps.Distribution.CRM.models import *


class ContactForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Contacts

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        widgets = {
            'customer': forms.HiddenInput(),
            'status': forms.HiddenInput(),
        }

