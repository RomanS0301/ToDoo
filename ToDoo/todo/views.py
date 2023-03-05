from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate


def home(request):
    return render(request, 'todo/home.html')

def signupuser(request):
    """
    Регистрация нового пользователя со страницы регистрации и добавление его в базу. Проверяется соответствие паролей и
    уникального имени пользователя. После регистрации на сайте, пользователь не может входить через админ панель

    """
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')  # переход на страницу пользователя

            except IntegrityError:
                return render(request, 'todo/signupuser.html',
                              {'form': UserCreationForm(), 'error': "Такое имя пользователя уже используется. "
                                                                    "Задайте новое имя пользователя."})

        else:
            return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': "Пароли не совпадают"})


def loginuser(request):
    """
    Вход пользователя
    """
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form': AuthenticationForm()})
    else:
        """ Проверка логина и пароля пользователя, если нет соответствия - возврат на страницу аутификации"""
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form': AuthenticationForm(), 'error': 'Введено неверное '
                                                                                                  'имя или пароль'})
        else:
            """При соответствии логина и пароля переход на страницу пользователя"""
            login(request, user)
            return redirect('currenttodos')


def logoutuser(request):
    """
    Выход пользователя из сети
    """
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def currenttodos(request):
    """Страница пользователя"""
    return render(request, 'todo/currenttodos.html')
