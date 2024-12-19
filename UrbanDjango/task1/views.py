from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .models import Buyer, Game
from .forms import ContactForm


def main(request: HttpRequest) -> HttpResponse:
    """Главная страница."""
    context = {
        'title': 'Главная страница',
    }
    return render(request, 'main.html', context)


def cart(request: HttpRequest) -> HttpResponse:
    """Корзина."""
    context = {
        'title': 'Корзина',
    }
    return render(request, 'cart.html', context)


def shop(request: HttpRequest) -> HttpResponse:
    """Магазин."""
    games = Game.objects.all()

    context = {
        'title': 'Игры',
        'games': games,
    }
    return render(request, 'shop.html', context)


def registration(request: HttpRequest,
                 username: str,
                 password: str,
                 repeat_password: str,
                 age: int,
                 form: ContactForm | None = None) -> HttpResponse:
    """Проверка введенных данных и регистрация пользователя"""
    # совпадение пароля
    if password != repeat_password:
        return render(request,
                      'registration_page.html',
                      {'answer': 'Пароли не совпадают', 'form': form})

    # проверка на возраст
    if age < 18:
        return render(request,
                      'registration_page.html',
                      {'answer': 'Вы должны быть старше 18 лет', 'form': form})

    # совпадение логина
    if Buyer.objects.filter(name=username):
        return render(request,
                      'registration_page.html',
                      {'answer': 'Пользователь уже существует', 'form': form})

    # добавление нового пользователя
    Buyer.objects.create(name=username, password=password, balance=500, age=age)

    return render(request,
                  'registration_page.html',
                  {'answer': f'Приветствуем {username}!', 'form': form})


def sign_up(request: HttpRequest) -> HttpResponse:
    """Страница регистрации"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():  # проверка заполненности всех полей
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            age = form.cleaned_data['age']

            return registration(request, username, password, repeat_password, age, form)

    else:
        form = ContactForm()

    return render(request,
                  'registration_page.html',
                  {'answer': 'Регистрация', 'form': form})
