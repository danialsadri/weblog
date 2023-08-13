from django import forms
from .models import *


class TicketForm(forms.Form):
    SUBJECT_CHOICES = (
        ('پیشنهاد', 'پیشنهاد'),
        ('انتقاد', 'انتقاد'),
        ('گزارش', 'گزارش'),
    )
    message = forms.CharField(widget=forms.Textarea, required=True, label='پیام')
    name = forms.CharField(max_length=200, required=True, label='نام')
    email = forms.EmailField(required=True, label='ایمیل')
    phone = forms.CharField(max_length=11, required=True, label='شماره تماس')
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES, label='موضوع')

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone:
            if not phone.isnumeric():
                raise forms.ValidationError('شماره تلفن عددی نیست')
            else:
                return phone


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'body']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'نام'}),
            'body': forms.Textarea(attrs={'placeholder': 'متن کامنت'})
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if name:
            if len(name) < 3:
                raise forms.ValidationError('نام کوتاه هست.')
            else:
                return name

    def clean_body(self):
        body = self.cleaned_data['body']
        if body:
            if len(body) > 300:
                raise forms.ValidationError('متن کامنت بیش ازحد مجاز است.')
            else:
                return body
