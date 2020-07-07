from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password

from scraping.models import City, Language

User = get_user_model()


class UserLoginForm(forms.Form):
    """Форма входу на сайт"""
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self, *args, **kwargs):
        """Перевірка на валідність"""
        email = self.cleaned_data.get('email').strip()
        password = self.cleaned_data.get('password').strip()

        if email and password:
            qs = User.objects.filter(email=email)
            if not qs.exists():
                raise forms.ValidationError('Такий користувач відсутній!')
            if not check_password(password, qs[0].password):
                raise forms.ValidationError('Невірний пароль!')
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError('Данний аккаунт заблоковано')
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegistrationForm(forms.ModelForm):
    """Форма регістрації"""
    email = forms.EmailField(label='Введіть email',
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Введіть пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Введіть пароль ще раз',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        data = self.cleaned_data
        if data['password'] != data['password2']:
            raise forms.ValidationError('Паролі не співпадають!')
        return data['password2']


class UserUpdateForm(forms.Form):
    """Данні аккаунта"""
    city = forms.ModelChoiceField(queryset=City.objects.all(), to_field_name="slug", required=True,
                                  widget=forms.Select(attrs={'class': 'form-control'}), label='місто')
    language = forms.ModelChoiceField(queryset=Language.objects.all(), to_field_name="slug", required=True,
                                      widget=forms.Select(attrs={'class': 'form-control'}), label='спеціальність')
    send_email = forms.BooleanField(required=False, widget=forms.CheckboxInput, label='отримати розсилку?')

    class Meta:
        model = User
        fields = ('city', 'language', 'send_email')


class ContactForm(forms.Form):
    """Форма зворотнього звязку"""
    city = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}), label='місто')
    language = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}),
                               label='спеціальність')
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}),
                             label='введіть email')
