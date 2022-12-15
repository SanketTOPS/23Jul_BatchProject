from django.contrib import admin
from django.urls import path,include
from myapp import views

urlpatterns = [
   path('',views.index),
   path('notes/',views.notes,name='notes'),
   path('userlogout/',views.userlogout),
   path('profile/',views.profile,name='profile'),
   path('about/',views.about),
   path('contact/',views.contact),
]