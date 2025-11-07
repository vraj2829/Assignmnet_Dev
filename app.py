import os
import django
from django.conf import settings
from django.urls import path
from django.shortcuts import render, redirect
from django.core.management import execute_from_command_line
from django.db import models

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

settings.configure(
    DEBUG=True,
    SECRET_KEY="abc123",
    ROOT_URLCONF=__name__,
    ALLOWED_HOSTS=["*"],
    INSTALLED_APPS=[
        "django.contrib.contenttypes",
        "django.contrib.staticfiles",
        "shop",  # app label
    ],
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    },
    TEMPLATES=[{
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
    }],
    DEFAULT_AUTO_FIELD="django.db.models.AutoField",
    STATIC_URL="/static/",
)

django.setup()

from shop.models import Product, Order


# --- Views ---
def home(request):
    products = Product.objects.all()
    return render(request, "home.html", {"products": products})

def about(request):
    return render(request, "about.html")

def products_view(request):
    products = Product.objects.all()
    return render(request, "products.html", {"products": products})

def buy(request, product_id):
    product = Product.objects.get(id=product_id)
    Order.objects.create(product=product)
    return redirect("/orders/")

def orders(request):
    orders = Order.objects.all()
    return render(request, "orders.html", {"orders": orders})

# --- URLs ---
urlpatterns = [
    path("", home),
    path("about/", about),
    path("products/", products_view),
    path("buy/<int:product_id>/", buy),
    path("orders/", orders),
]

# --- Run Server ---
if __name__ == "__main__":
    from django.core.management import call_command

    call_command("makemigrations", "shop", interactive=False)
    call_command("migrate", interactive=False)

    # Seed products
    if not Product.objects.exists():
        Product.objects.create(name="Laptop", price=899.99, description="A powerful laptop")
        Product.objects.create(name="Headphones", price=49.99, description="Noise-cancelling headphones")
        Product.objects.create(name="Smartphone", price=499.99, description="Latest smartphone")
        Product.objects.create(name="Smartwatch", price=199.99, description="Fitness smartwatch")

    execute_from_command_line(["manage.py", "runserver", "0.0.0.0:8000"])
