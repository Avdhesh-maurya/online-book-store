from django.shortcuts import render,redirect
from django.contrib import messages
from mainapp.models import * 
from django.contrib import messages
from .models import *
from userapp.models import *
from django.views.decorators.cache import cache_control
# Create your views here.
@cache_control(no_cache=True, no_store =True,must_revalidate=True)
def admindash(request):
    if 'adminid' not in request.session:
        messages.error(request,'Session Timed Out')
        return redirect('adminlogin')
    adminid=request.session.get('adminid')
    ad=LoginInfo.objects.get(username=adminid)
    context={
        'adminid':adminid,
        'ad':ad,
        'usercount':UserInfo.objects.all().count(),
        'bookcount':Book.objects.all().count(),
        'catcount':Category.objects.all().count(),
        'ordercount':Book.objects.all().count(),
        'enquirycount':Enquiry.objects.all().count()
    }
    return render(request,'admindash.html',context)
def adminlogout(request):
    if 'adminid' in request.session:
        del request.session['adminid']
        messages.success(request,'You are logged out')
        return redirect('adminlogin')
    else:
        return redirect('adminlogin')
@cache_control(no_cache=True, no_store =True,must_revalidate=True)
def viewenqs(request):
    if 'adminid' not in request.session:
        messages.error(request,'Session Timed Out')
        return redirect('adminlogin')
    adminid=request.session.get('adminid')
    enq=Enquiry.objects.all()
    context={
        'adminid':adminid,
        'enq':enq,
    }
    
    return render(request,'viewenqs.html',context)
def delenqs(request,id):
    if 'adminid' not in request.session:
        messages.error(request,'Session Timed Out')
        return redirect('adminlogin')
    adminid=request.session.get('adminid')
    enq=Enquiry.objects.get(id=id)
    enq.delete()
    messages.success(request,"Successfully Deleted")
    return redirect('viewenqs')
@cache_control(no_cache=True, no_store =True,must_revalidate=True)
def addcat(request):
    if 'adminid' not in request.session:
        messages.error(request,'Session Timed Out')
        return redirect('adminlogin')
    adminid=request.session.get('adminid')
    context={
        'adminid':adminid,
    }
    if request.method == "POST":
        name=request.POST.get('name')
        description=request.POST.get('description')
        try:
            temp=Category.objects.get(name=name)
            if temp:
                messages.error(request,"Already Existing Category.")
        except Category.DoesNotExist:

            
            cat=Category(name=name,description=description)
            cat.save()
            messages.success(request,"Category Added Successfully")
            return redirect('addcat')
    return render(request,'addcat.html',context)
@cache_control(no_cache=True, no_store =True,must_revalidate=True)
def viewcat(request):
    if 'adminid' not in request.session:
        messages.error(request,'Session Timed Out')
        return redirect('adminlogin')
    adminid=request.session.get('adminid')
    cat=Category.objects.all()
    context={
        'adminid':adminid,
        'cat':cat,
    }
    return render(request,'viewcat.html',context)
@cache_control(no_cache=True, no_store =True,must_revalidate=True)
def addbook(request):
    if 'adminid' not in request.session:
        messages.error(request,'Session Timed Out')
        return redirect('adminlogin')
    adminid=request.session.get('adminid')
    cats=Category.objects.all()
    context={
        'adminid':adminid,
        'cats':cats,
    }
    if request.method=="POST":
        title=request.POST.get('title')
        author=request.POST.get('author')
        category=request.POST.get('category')
        cats= Category.objects.get(id=category)   #check it and it must be added
        description=request.POST.get('description')
        original_price=request.POST.get('original_price')
        price=request.POST.get('price')
        published_date=request.POST.get('published_date')
        language=request.POST.get('language')
        cover_image=request.FILES.get('cover_image')
        stock=request.POST.get('stock')
        try:
            temp=Book.objects.get(title=title)
            if temp:
                messages.error(request,"Already Existing Book")
                redirect('addbook')
            
        except Book.DoesNotExist:
            b=Book(
            title=title,
            author=author,
            category=cats,
            description=description,
            original_price=original_price,
            price=price,
            publish_date=published_date,
            language=language,
            cover_image=cover_image,
            stock=stock
            )

        
            b.save()
            messages.success(request,"Book added successfully")
            return redirect('addbook')
    return render(request, 'addbook.html',context)
@cache_control(no_cache=True, no_store =True,must_validate=True)
def viewbook(request): #viewbook
    if 'adminid' not in request.session:
        messages.error(request, "You are not logged in")
        return redirect('adminlogin')
    adminid= request.session.get('adminid')####
    book=Book.objects.all()
    context={
        'adminid':adminid,
        'book':book,
    }
    return render(request, 'viewbook.html',context)
def delcat(request,id):
    if 'adminid' not in request.session:
        messages.error(request,'Session Timed Out')
        return redirect('adminlogin')
    adminid=request.session.get('adminid')
    cat=Category.objects.get(id=id)
    cat.delete()
    messages.success(request,"Successfully Deleted")
    return redirect('viewcat')
def delbook(request,id):
    if 'adminid' not in request.session:
        messages.error(request,'Session Timed Out')
        return redirect('adminlogin')
    adminid=request.session.get('adminid')
    book=Book.objects.get(id=id)
    book.delete()
    messages.success(request,"Successfully Deleted")
    return redirect('viewbook')

def changepassword(request):
    if 'adminid' not in request.session:
        messages.error(request,"You are not logged in.")
        return redirect('adminlogin')
    adminidd=request.session.get('adminid')
    info=LoginInfo.objects.get(username=adminidd)
    
    context={
        'adminid':adminidd,
        'info':info,
        
    }
    
    if request.method=="POST":
        
        if info:
            passs=request.POST.get('oldpassword')
            if(passs!=info.password):
                messages.error(request,"Incorrect Old Password")
                return redirect('changepassword')
            npasss=request.POST.get('newpassword')
            if(passs==npasss):
                messages.error(request,"Old and new password should not be same")
                return redirect('changepassword')
            cn=request.POST.get('confirmpassword')
            if npasss!=cn:
                messages.error(request,"confirm password and new password are not same")
                return redirect('changepassword')
            info.password=npasss
            info.save()
            messages.success(request,"Password changed Successfully")
            return redirect('changepassword')
        else:
            messages.error(request,"Not such entry found")
            return redirect('changepassword')
    return render(request,'changepassword.html',context)
@cache_control(no_cache=True, no_store =True,must_revalidate=True)
def editbook(request,id):
    if 'adminid' not in request.session:
        messages.error(request,'Session Timed Out')
        return redirect('adminlogin')
    adminid=request.session.get('adminid')
    book=Book.objects.get(id=id)
    cats=Category.objects.all()
    context={
        'adminid':adminid,
        'book':book,
        'cats':cats,
    }
    if request.method=="POST":
        title=request.POST.get('title')
        author=request.POST.get('author')
        category=request.POST.get('category')
        cats= Category.objects.get(id=category)   #check it and it must be added
        description=request.POST.get('description')
        original_price=request.POST.get('original_price')
        price=request.POST.get('price')
        published_date=request.POST.get('published_date')
        language=request.POST.get('language')
        cover_image=request.FILES.get('cover_image')
        stock=request.POST.get('stock')
        book.title=title
        book.author=author
        book.category=cats
        book.description=description
        book.original_price=original_price
        book.price=price
        if published_date:
            book.publish_date=published_date
        book.language=language
        if cover_image:
            book.cover_image=cover_image
        book.stock=stock
        book.save()
        messages.success(request,"Successfully Updated")
        return redirect('viewbook')
    return render(request,'editbook.html',context)
