from django import forms

from coop.messaging.models import Message


class MessagingForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['request', 'note']
        labels = {
            'request': "Request",
            'note': "Note",
        }
        widgets = {
            'note': forms.TextInput(attrs={'placeholder': 'Enter here a note for helping execute the request '
                                                          '(eg: Cooperative Name)'}),
        }
