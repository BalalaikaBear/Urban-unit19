from django import forms


class ContactForm(forms.Form):
    username = forms.CharField(max_length=30, label='Логин')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    repeat_password = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    age = forms.IntegerField(max_value=999, label='Возраст')
