import datetime as dt
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages

from accounts.forms import (UserLoginForm, UserRegistrationForm,
                            UserUpdateForm, ContactForm)
from scraping.models import Error

User = get_user_model()


def login_view(request):
    """Ідентифікація"""
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email=email, password=password)
        login(request, user)
        return redirect('/')
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """Вихід із системи"""
    logout(request)
    return redirect('/')


def register_view(request):
    """Регістрація"""
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()
        messages.success(request, 'Користувач добавлений в систему.')
        return render(request, 'accounts/register_done.html', {'new_user': new_user})
    return render(request, 'accounts/register.html', {'form': form})


def update_view(request):
    """Зміна налаштувань з перевіркою на валідність користувача"""
    contact_form = ContactForm()
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            form = UserUpdateForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user.city = data['city']
                user.language = data['language']
                user.send_email = data['send_email']
                user.save()
                messages.success(request, 'Данні збережені.')
                return redirect('accounts:update')

        form = UserUpdateForm(
            initial={'city': user.city, 'language': user.language,
                     'send_email': user.send_email})
        return render(request, 'accounts/update.html',
                      {'form': form, 'contact_form': contact_form})
    else:
        return redirect('accounts:login')


def delete_view(request):
    """Видалення користувача"""
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            qs = User.objects.get(pk=user.pk)
            qs.delete()
            messages.error(request, 'Користувача видалено :(')
    return redirect('/')


def contact(request):
    """Зворотній звязок"""
    if request.method == 'POST':
        contact_form = ContactForm(request.POST or None)
        if contact_form.is_valid():
            data = contact_form.cleaned_data
            city = data.get('city')
            language = data.get('language')
            email = data.get('email')
            qs = Error.objects.filter(timestamp=dt.date.today())
            if qs.exists():
                err = qs.first()
                data = err.data.get('user_data', [])
                data.append({'city': city, 'email': email, 'language': language})
                err.data['user_data'] = data
                err.save()
            else:
                data = [{'city': city, 'email': email, 'language': language}]
                Error(data=f"user_data:{data}").save()
            messages.success(request, 'Данні відправлені адміністрації.')
            return redirect('accounts:update')
        else:
            return redirect('accounts:update')
    else:
        return redirect('accounts:login')
