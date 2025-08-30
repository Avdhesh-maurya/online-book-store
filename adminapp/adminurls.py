from django.urls import path
from . import views

urlpatterns = [
    path("admindash/", views.admindash, name="admindash"),
    path("adminlogout/", views.adminlogout, name="adminlogout"),
    path("viewenqs/", views.viewenqs, name="viewenqs"),
    path("delenqs/<int:id>", views.delenqs, name="delenqs"),
    path("addcat/", views.addcat, name="addcat"),
    path("viewcat/", views.viewcat, name="viewcat"),
    path("viewbook/", views.viewbook, name="viewbook"),
    path("addbook/", views.addbook, name="addbook"),
    path("delcat/<int:id>", views.delcat, name="delcat"),
    path("delbook/<int:id>", views.delbook, name="delbook"),
    path("changepassword/", views.changepassword, name="changepassword"),
    path("editbook/<int:id>", views.editbook, name="editbook"),
]
