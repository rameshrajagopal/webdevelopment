from __future__ import absolute_import

from django import forms

import datetime
from django.utils.timezone import utc
from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit

from . import models

class TalkListForm(forms.ModelForm):
    class Meta:
        fields = ('name',)
        model = models.TalkList

    def __init__(self, *args, **kwargs):
        super(TalkListForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
                'name',
                ButtonHolder(
                    Submit('create', 'Create', css_class='btn-primary')
                    )
                )

class TalkForm(forms.ModelForm):
    class Meta:
        fields = ('name', 'host', 'when', 'room',)
        model  = models.Talk

    def __init__(self, *args, **kwargs):
        super(TalkForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
                'name', 'host', 'when', 'room',
                ButtonHolder(
                    Submit('add', 'Add', css_class='btn-primary')
                    )
                )
    def clean_when(self):
         when = self.cleaned_data.get('when')
         start = datetime.datetime(2015, 5, 5).replace(tzinfo=utc)
         end   = datetime.datetime(2015, 5, 10).replace(tzinfo=utc)
         if not start < when < end:
            raise ValidationError("'when' is outside of date")
         return when




