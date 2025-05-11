from django import forms
from django.contrib.auth.models import User

class ContactForm(forms.Form):
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'w-full rounded-lg border border-gray-200 px-4 py-2.5 focus:border-amber-400 focus:outline-none focus:ring-1 focus:ring-amber-400'
        })
    )
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'w-full rounded-lg border border-gray-200 px-4 py-2.5 focus:border-amber-400 focus:outline-none focus:ring-1 focus:ring-amber-400'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full rounded-lg border border-gray-200 px-4 py-2.5 focus:border-amber-400 focus:outline-none focus:ring-1 focus:ring-amber-400'
        })
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full rounded-lg border border-gray-200 px-4 py-2.5 focus:border-amber-400 focus:outline-none focus:ring-1 focus:ring-amber-400'
        })
    )
    subject = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full rounded-lg border border-gray-200 px-4 py-2.5 focus:border-amber-400 focus:outline-none focus:ring-1 focus:ring-amber-400'
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 5,
            'class': 'w-full rounded-lg border border-gray-200 px-4 py-2.5 focus:border-amber-400 focus:outline-none focus:ring-1 focus:ring-amber-400'
        })
    )