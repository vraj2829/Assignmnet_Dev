import os
import django
from django.conf import settings
from django.urls import path
from django.shortcuts import render, redirect
from django.core.management import execute_from_command_line
from django.db import models
from django.contrib import admin

from django.urls import path, include

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

settings.configure(
    DEBUG=True,
    SECRET_KEY="abc123",
    ROOT_URLCONF=__name__,
    ALLOWED_HOSTS=["*"],

    INSTALLED_APPS=[
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "shop",
    ],

    MIDDLEWARE=[
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
    ],

    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    },

   
    CSRF_TRUSTED_ORIGINS=[
        "https://redapple-egop.onrender.com",
        "http://localhost:8000",
    ],

    TEMPLATES=[{
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }],

    DEFAULT_AUTO_FIELD="django.db.models.AutoField",
    STATIC_URL="/static/",

    # ✅ Add login redirects to fix login/logout
    LOGIN_URL="/accounts/login/",
    LOGIN_REDIRECT_URL="/",
    LOGOUT_REDIRECT_URL="/",
)


django.setup()

from shop.models import Product, Order
from django.contrib.auth.models import User  # <-- Add this

# --- CREATE SUPERUSER HERE ---
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="admin123"
    )
    print("Superuser created: username='admin', password='admin123'")

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
    path("admin/", admin.site.urls),
    path("", include("shop.urls")),  # include shop app URLs
    # Add this to enable login/logout pages
    
]




# --- Run Server ---
if __name__ == "__main__":
    from django.core.management import call_command

    call_command("makemigrations", "shop", interactive=False)
    call_command("migrate", interactive=False)


# Seed 20 car products with valid images
products_to_add = [
    {"name": "Tesla Model S", "price": 89999.99, "description": "Electric luxury sedan", "image": "https://images.pexels.com/photos/358070/pexels-photo-358070.jpeg"},
    {"name": "Ford Mustang", "price": 55999.99, "description": "Iconic American muscle car", "image": "https://www.ford.com/acslibs/content/dam/na/ford/en_us/images/mustang/2026/jellybeans/26_frd_mst_gtp_orfy_ps34_v1.png"},
    {"name": "BMW X5", "price": 61999.99, "description": "Luxury SUV with performance", "image": "https://images.pexels.com/photos/1149831/pexels-photo-1149831.jpeg"},
    {"name": "Audi A6", "price": 53999.99, "description": "Premium executive sedan", "image": "https://images.autox.com/uploads/2019/10/16-500x261.jpg"},
    {"name": "Mercedes-Benz GLE", "price": 68999.99, "description": "Luxury SUV with style", "image": "https://vehicle-images.dealerinspire.com/1433-110012062/thumbnails/large/4JGFD6BB2SB383992/aa7f2aa6e9e50a612dbb1fa290bdf403.jpg"},
    {"name": "Porsche 911", "price": 120999.99, "description": "Legendary sports car", "image": "https://images.pexels.com/photos/164634/pexels-photo-164634.jpeg"},
    {"name": "Chevrolet Camaro", "price": 42999.99, "description": "American muscle with power", "image": "https://images.pexels.com/photos/1149833/pexels-photo-1149833.jpeg"},
    {"name": "Honda Civic", "price": 23999.99, "description": "Reliable compact sedan", "image": "https://media.ed.edmunds-media.com/honda/civic/2026/oem/2026_honda_civic_sedan_si_fq_oem_1_1280.jpg"},
    {"name": "Toyota Corolla", "price": 21999.99, "description": "Economical and reliable sedan", "image": "https://www.exoticcarhacks.com/wp-content/uploads/2024/02/D-8WJU7I-scaled.jpeg"},
    {"name": "Jeep Wrangler", "price": 39999.99, "description": "Off-road adventure SUV", "image": "https://media.ed.edmunds-media.com/jeep/wrangler/2025/oem/2025_jeep_wrangler_convertible-suv_rubicon-x_fq_oem_1_1280.jpg"},
    {"name": "Lamborghini Huracan", "price": 250999.99, "description": "Exotic Italian sports car", "image": "https://www.exoticcarhacks.com/wp-content/uploads/2024/02/D-8WJU7I-scaled.jpeg"},
    {"name": "Ferrari F8", "price": 320999.99, "description": "Italian supercar excellence", "image": "https://vdmcars.com/media/o0dbzyaw/efd2135f-ee6d-4051-ada2-809ab24aade5-rule-mo-1600.jpg"},
    {"name": "Range Rover", "price": 89999.99, "description": "Luxury SUV with comfort", "image": "https://res.cloudinary.com/unix-center/image/upload/c_limit,dpr_3.0,f_auto,fl_progressive,g_center,h_580,q_75,w_906/n20onzdjgzcnueh01av5.jpg"},
    {"name": "Kia Sportage", "price": 28999.99, "description": "Compact SUV with style", "image": "https://s37629.pcdn.co/wp-content/uploads/2021/11/2023-Kia-Sportage-Hybrid-Hero-1400.jpg"},
    {"name": "Mazda CX-5", "price": 30999.99, "description": "Stylish crossover SUV", "image": "https://images.pexels.com/photos/1149831/pexels-photo-1149831.jpeg"},
    {"name": "Volkswagen Golf", "price": 26999.99, "description": "Compact hatchback with style", "image": "https://www.v3cars.com/media/model-imgs/661912Volkswagen-Golf-GTI.webp"},
    {"name": "Nissan Altima", "price": 24999.99, "description": "Reliable mid-size sedan", "image": "https://images.pexels.com/photos/1149831/pexels-photo-1149831.jpeg"},
    {"name": "Subaru Outback", "price": 33999.99, "description": "Adventure-ready wagon", "image": "https://media.ed.edmunds-media.com/subaru/outback/2026/oem/2026_subaru_outback_4dr-suv_touring-xt_fq_oem_1_1280.jpg"},
    {"name": "Mitsubishi Outlander", "price": 27999.99, "description": "Versatile family SUV", "image": "https://media.ed.edmunds-media.com/honda/civic/2026/oem/2026_honda_civic_sedan_si_fq_oem_1_1280.jpg"},
    {"name": "Hyundai Tucson", "price": 28999.99, "description": "Modern compact SUV", "image": "https://media.ed.edmunds-media.com/jeep/wrangler/2025/oem/2025_jeep_wrangler_convertible-suv_rubicon-x_fq_oem_1_1280.jpg"},
]



# --- Remove old products ---
#Product.objects.all().delete()


for p in products_to_add:
    Product.objects.get_or_create(name=p["name"], defaults=p)


execute_from_command_line(["manage.py", "runserver", "0.0.0.0:8000"])
