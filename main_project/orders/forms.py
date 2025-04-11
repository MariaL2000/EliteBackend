from django import forms
from .models import Order, Comment, Schedule
import re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'opinion', 'rating', 'sug']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name'}),
            'opinion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'What do you think?'}),
            'rating': forms.RadioSelect(choices=[(i, '★' * i + '☆' * (5 - i)) for i in range(0, 6)]),  # Ajuste para permitir 0 estrellas
            'sug': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Do you have suggestions?'})
        }


class ClientOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['client_name', 'description', 'phone', 'email', 'address']
        widgets = {
            'client_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Tell us more about your project...'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your phone'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your@email.com'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your address'}),
        }

   

    def clean_client_name(self):
        client_name = self.cleaned_data.get('client_name')
        if len(client_name) < 8:
            raise forms.ValidationError('Client name must be at least 5 characters long.')
        return client_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError('Enter a valid email address.')
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.match(r'^\d+$', phone):
            raise forms.ValidationError('Phone number must contain only digits.')
        return phone
    
    def clean_description(self):
        description = self.cleaned_data.get('description')
        if not description:
            raise forms.ValidationError('Description is required.')
        return description

class ScheduleSelectionForm(forms.Form):
    schedule = forms.ModelChoiceField(queryset=Schedule.objects.filter(is_available=True), required=True, label="Select Schedule")





class OrderForm(forms.ModelForm):
    schedule = forms.ModelChoiceField(
        queryset=Schedule.objects.filter(is_available=True),
         widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta(ClientOrderForm.Meta):
        fields = ClientOrderForm.Meta.fields + ['schedule']










from django import forms
from .models import SiteConfiguration
from django.contrib import admin

class SiteConfigurationForm(forms.ModelForm):
    class Meta:
        model = SiteConfiguration
        fields = '__all__'
        widgets = {
            'background_color': forms.TextInput(attrs={'class': 'jscolor'}),
            'text_color': forms.TextInput(attrs={'class': 'jscolor'}),
            'button_color': forms.TextInput(attrs={'class': 'jscolor'}),
            'button_text_color': forms.TextInput(attrs={'class': 'jscolor'}),
        }
