from django.shortcuts import render, redirect
from django.contrib import messages
from mainapp.models import *
from adminapp.models import *
from .models import *

# Payment
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.cache import cache_control

# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def userdash(request):
    if "userid" not in request.session:
        messages.error(request, "You are not logged in.")
        return redirect("login")
    userid = request.session.get("userid")
    user = UserInfo.objects.get(email=userid)
    orders = OrderItem.objects.all().count()
    totalamount = 0
    for i in OrderItem.objects.all():
        totalamount += i.price

    context = {
        "userid": userid,
        "user": user,
        "orders": orders,
        "totalamount": totalamount,
        "cartitem": CartItem.objects.all().count(),
    }
    return render(request, "userdash.html", context)


def userlogout(request):
    if "userid" in request.session:
        del request.session["userid"]
        messages.success(request, "Logged out successfully.")
        return redirect("index")
    else:
        messages.error(request, "Login First")
        return redirect("index")


@cache_control(no_cache=True, no_store=True, must_validate=True)
def userprofile(request):
    if "userid" not in request.session:
        messages.error(request, "You are not logged in.")
        return redirect("login")
    userid = request.session.get("userid")
    user = UserInfo.objects.get(email=userid)
    context = {
        "userid": userid,
        "user": user,
    }
    return render(request, "userprofile.html", context)


@cache_control(no_cache=True, no_store=True, must_validate=True)
def editprofile(request):
    if "userid" not in request.session:
        messages.error(request, "You are not logged in.")
        return redirect("login")
    userid = request.session.get("userid")
    em = request.session.get("email")
    log = LoginInfo.objects.get(username=userid)
    user = UserInfo.objects.get(email=log.username)
    context = {
        "userid": userid,
        "user": user,
    }
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        picture = request.FILES.get("pic")
        email = request.POST.get("email")
        address = request.POST.get("address")
        user.name = name
        user.phone = phone
        if picture:
            user.profile = picture
        user.email = email
        user.address = address
        user.save()
        messages.success(request, "Changed Succcessfully.")
        return redirect("userdash")
    return render(request, "editprofile.html", context)


@cache_control(no_cache=True, no_store=True, must_validate=True)
def viewcart(request):
    if "userid" not in request.session:
        messages.error(request, "You are not logged in.")
        return redirect("login")
    userid = request.session.get("userid")
    user = UserInfo.objects.get(email=userid)
    ucart = Cart.objects.filter(user=user)
    if not ucart.exists():
        Cart.objects.create(user=user)
    cart = Cart.objects.get(user=user)
    items = CartItem.objects.filter(cart=cart)
    totalamount = 0
    for i in items:
        totalamount += i.get_total_price()
    context = {
        "userid": userid,
        "user": user,
        "items": items,
        "totalamount": totalamount,
    }
    return render(request, "viewcart.html", context)


@cache_control(no_cache=True, no_store=True, must_validate=True)
def userorders(request):
    if "userid" not in request.session:
        messages.error(request, "You are not logged in.")
        return redirect("login")
    userid = request.session.get("userid")
    user = UserInfo.objects.get(email=userid)
    orders = Order.objects.filter(user=user)
    orderitems = []
    for o in orders:
        orderitems.append(OrderItem.objects.filter(order=o))
    context = {
        "userid": userid,
        "user": user,
        "orderitems": orderitems,
    }
    return render(request, "userorders.html", context)


def changeuserpassword(request):
    if "userid" not in request.session:
        messages.error(request, "You are not logged in.")
        return redirect("login")
    useridd = request.session.get("userid")
    info = LoginInfo.objects.get(username=useridd, usertype="user")

    context = {
        "userid": useridd,
        "info": info,
    }

    if request.method == "POST":

        if info:
            passs = request.POST.get("oldpassword")
            if passs != info.password:
                messages.error(request, "Incorrect Old Password")
                return redirect("changeuserpassword")
            npasss = request.POST.get("newpassword")
            if passs == npasss:
                messages.error(request, "Old and new password should not be same")
                return redirect("changeuserpassword")
            cn = request.POST.get("confirmpassword")
            if npasss != cn:
                messages.error(
                    request, "confirm password and new password are not same"
                )
                return redirect("changeuserpassword")
            info.password = npasss
            info.save()
            messages.success(request, "Password changed Successfully")
            return redirect("changeuserpassword")
        else:
            messages.error(request, "Not such entry found")
            return redirect("changeuserpassword")
    return render(request, "changeuserpassword.html", context)


def addtocart(request, id):
    if "userid" not in request.session:
        messages.error(request, "You are not logged in.")
        return redirect("login")
    userid = request.session.get("userid")
    user = UserInfo.objects.get(email=userid)
    ucart = Cart.objects.filter(user=user)
    if not ucart.exists():
        Cart.objects.create(user=user)
    ucart = Cart.objects.get(user=user)
    book = Book.objects.get(id=id)
    if request.method == "POST":
        quantity = request.POST.get("quantity")
        if quantity is None:
            quantity = 1
        ci = CartItem(cart=ucart, book=book, quantity=quantity)
        ci.save()
        messages.success(request, "Added to cart.")
        return redirect("viewcart")
    else:
        messages.error(request, "Invalid Operation")
        return redirect("index")


def removeitems(request, id):
    if "userid" not in request.session:
        messages.error(request, "You are not logged in.")
        return redirect("login")
    userid = request.session.get("userid")
    user = UserInfo.objects.get(email=userid)
    ci = CartItem.objects.get(id=id)
    ci.delete()
    messages.success(request, "Book remover from cart")
    return redirect("viewcart")


# Payment Functions.
def checkout(request):
    if "userid" not in request.session:
        messages.error(request, "You are not logged in")
        return redirect("login")

    userid = request.session.get("userid")
    user = UserInfo.objects.get(email=userid)
    cart = Cart.objects.get(user=user)
    items = CartItem.objects.filter(cart=cart)

    line_items = []

    for item in items:
        line_items.append(
            {
                "price_data": {
                    "currency": "inr",
                    "unit_amount": int(item.book.price * 100),
                    "product_data": {
                        "name": item.book.title,
                    },
                },
                "quantity": item.quantity,
            }
        )

    session = stripe.checkout.Session.create(
        payment_method_types=["card", "sepa_debit"],
        line_items=line_items,
        mode="payment",
        success_url=request.build_absolute_uri("/userapp/payment-success/"),
        cancel_url=request.build_absolute_uri("/viewcart/"),
    )

    return redirect(session.url, code=303)


def payment_success(request):
    if "userid" not in request.session:
        messages.error(request, "Please login first.")
        return redirect("login")

    userid = request.session.get("userid")
    user = UserInfo.objects.get(email=userid)

    try:
        cart = Cart.objects.get(user=user)
        cart_items = CartItem.objects.filter(cart=cart)

        if not cart_items.exists():
            messages.warning(request, "No items found in your cart.")
            return redirect("index")

        total_amount = sum(item.get_total_price() for item in cart_items)
        order = Order.objects.create(user=user, total_amount=total_amount)

        # Create order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                book=item.book,
                quantity=item.quantity,
                price=item.book.price,
            )
            book = Book.objects.get(id=item.book.id)
            book.stock = book.stock - item.quantity
            book.save()

        cart_items.delete()

        items = OrderItem.objects.filter(order=order)

        # Add total_price attribute to each item
        for item in items:
            item.total_price = item.quantity * item.price

        messages.success(request, "Payment successful! Your order has been placed.")
        return render(request, "payment_success.html", {"order": order})

    except Cart.DoesNotExist:
        messages.error(request, "Cart not found.")
        return redirect("index")
