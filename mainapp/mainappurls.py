from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("adminlogin/", views.adminlogin, name="adminlogin"),
    path("adminlog/", views.adminlog, name="adminlog"),
    path("book_details/<id>", views.book_details, name="book_details"),
    path("search/", views.search, name="search"),
]
