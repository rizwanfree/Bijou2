from django import forms
from django.core.mail import EmailMessage
from .widgets import MultipleFileInput  # Import the custom widget

class ComposeEmailForm(forms.Form):
    recipient = forms.EmailField()
    subject = forms.CharField(max_length=100)
    body = forms.CharField(widget=forms.Textarea)
    attachments = forms.FileField(
        widget=MultipleFileInput(),
        required=False,
        label='Attachments'
    )

    def send_email(self):
        email = EmailMessage(
            subject=self.cleaned_data['subject'],
            body=self.cleaned_data['body'],
            to=[self.cleaned_data['recipient']]
        )
        
        if self.cleaned_data.get('attachments'):
            for attachment in self.cleaned_data['attachments']:
                email.attach(
                    attachment.name,
                    attachment.read(),
                    attachment.content_type
                )
        email.send()