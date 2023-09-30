from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from cart.forms import CartAddProductForm
from .forms import RegisterUserForm, LoginUserForm
from .models import Product


# Create your views here.

class AllProducts(ListView):
    model = Product
    extra_context = {"title": "Игрушки"}


# class HomePage()

def index(request):
    context = {
        "title": "Toy Factory"
    }
    return render(request, 'gshop/index.html', context=context)


def about(request):
    context = {
        "title": "О нас",
    }
    return render(request, 'gshop/about.html', context=context)


def news(request):
    context = {
        "title": "Новости",
    }
    return render(request, 'gshop/news.html', context=context)

def faq(request):
    context = {
        "title": "FAQ",
    }
    return render(request, 'gshop/faq.html', context=context)

def contacts(request):
    context = {
        "title": "Контакты"
    }
    return render(request, 'gshop/contacts.html', context=context)

def privacy_policy(request):
    context = {
        "title": "Политика конфиденциальности"
    }
    return render(request, 'gshop/privacy_policy.html', context=context)

def vacancies(request):
    context = {
        "title": "Вакансии"
    }
    return render(request, 'gshop/vacancies.html', context=context)

def reviews(request):
    context = {
        "title": "Отзывы"
    }
    return render(request, 'gshop/reviews.html', context=context)

def coupons(request):
    context = {
        "title": "Купоны"
    }
    return render(request, 'gshop/coupons.html', context=context)

class CatProducts(ListView):
    model = Product
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cat_selected'] = context['object_list'][0].category_id
        context['title'] = str(context['object_list'][0].category)
        return context

    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs['category_slug'], is_available=True)


class UnoProduct(DetailView):
    model = Product
    slug_url_kwarg = 'product_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_form'] = CartAddProductForm()
        context['title'] = str(context['object'].name)
        return context

    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs['category_slug'],
                                      slug=self.kwargs['product_slug'], is_available=True)


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'gshop/register.html'
    success_url = reverse_lazy('login')
    extra_context = {"title": "Регистрация"}

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('all_products')



class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'gshop/login.html'
    extra_context = {"title": "Welcome!"}



def logout_user(request):
    logout(request)
    return redirect('home')
