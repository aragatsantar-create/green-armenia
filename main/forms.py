from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Volunteer

class VolunteerForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = ['name', 'email', 'phone', 'message']
        labels = {
            'name': _('Ваше имя'),
            'email': _('Email'),
            'phone': _('Телефон'),
            'message': _('Сообщение'),
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': _('Введите ваше имя'),
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': _('Введите ваш email'),
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': _('Введите ваш телефон (необязательно)')
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': _('Расскажите о себе и почему хотите присоединиться'),
                'rows': 5
            }),
        }