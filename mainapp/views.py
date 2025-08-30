from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
from adminapp.models import *


def index(request):
    books = Book.objects.all()
    userid = request.session.get("userid")
    context = {
        "books": books,
        "userid": userid,
    }
    return render(request, "index.html", context)


def about(request):
    context = {"userid": request.session.get("userid")}
    return render(request, "about.html", context)


def base(request):
    context = {"userid": request.session.get("userid")}
    return render(request, "base.html", context)


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        enq = Enquiry(
            name=name, email=email, phone=phone, subject=subject, message=message
        )
        enq.save()
        messages.success(request, "Submitted Successfully")

        return redirect("contact")
    context = {"userid": request.session.get("userid")}
    return render(request, "contact.html", context)


def register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        cpassword = request.POST.get("confirmpassword")
        if password != cpassword:
            messages.error(request, "Password and confirm password should be same.")
            return redirect("register")
        ch = LoginInfo.objects.filter(username=email)
        if ch:
            messages.error(request, "Email Already Exist")
            return redirect("register")
        log = LoginInfo(usertype="user", username=email, password=password)
        user = UserInfo(name=name, email=email, phone=phone, login=log)
        log.save()
        user.save()
        messages.success(request, "Account Created....")
        return redirect("register")
    context = {"userid": request.session.get("userid")}
    return render(request, "register.html", context)


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = LoginInfo.objects.get(
                username=username, password=password, usertype="user"
            )
            if user is not None:
                request.session["userid"] = username
                messages.success(request, "Welcome User")
                return redirect("index")

        except LoginInfo.DoesNotExist:
            messages.error(request, "Invalid Credentials")
            return redirect("login")
    context = {"userid": request.session.get("userid")}
    return render(request, "login.html", context)


def dashboard(request):
    return render(request, "dashboard.html")


def adminlogin(request):

    return render(request, "adminlogin.html")


def adminlog(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            admin = LoginInfo.objects.get(
                username=username, password=password, usertype="admin"
            )
            if admin is not None:
                request.session["adminid"] = username
                messages.success(request, "Admin Login Successful.")
                return redirect("admindash")
        except LoginInfo.DoesNotExist:
            messages.error(request, "Invalid Credentials")
            return redirect("adminlogin")
    else:
        return redirect("adminlogin")


def book_details(request, id):
    context = {"book": Book.objects.get(id=id)}
    return render(request, "book_details.html", context)


def search(request):
    titlee = request.GET.get("search")
    booktitle = Book.objects.filter(title__icontains=titlee)
    bookauthor = Book.objects.filter(author__icontains=titlee)
    bookdesc = Book.objects.filter(description__icontains=titlee)
    searc = booktitle.union(bookauthor)
    search = searc.union(bookdesc)
    us = request.session.get("userid")
    context = {
        "search": search,
        "us": us,
    }
    return render(request, "search.html", context)


# Create your views here.
