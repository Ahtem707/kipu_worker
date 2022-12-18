from django.forms import ModelForm, TextInput, NumberInput, EmailInput, DateTimeInput, HiddenInput

from .models import Users


class UsersForm(ModelForm):
    class Meta:
        model = Users
        fields = ['telegram_id', 'sername', 'gender', 'phone', 'birthday', 'mail']

        widgets = {
            'telegram_id': HiddenInput(attrs={
                'class': 'form-contol',
                'id': 'telegram_id'
            }),
            'sername': TextInput(attrs={
                'class': 'form-contol',
                'placeholder': 'Имя'
            }),
            "gender": TextInput(attrs={
                'class': 'form-contol',
                'placeholder': 'Пол'
            }),
            "phone": NumberInput(attrs={
                'class': 'form-contol',
                'placeholder': 'Номер телефона'
            }),
            "birthday": DateTimeInput(attrs={
                'class': 'form-contol',
                'placeholder': 'Дата рождения'
            }),
            "mail": EmailInput(attrs={
                'class': 'form-contol',
                'placeholder': 'Почта'
            }),
        }
