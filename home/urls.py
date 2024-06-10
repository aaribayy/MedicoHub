from django.contrib import admin
from django.urls import path, include
from home import views


urlpatterns = [
    path('',views.index, name='home'),
    path('about/',views.about, name='about'),
    path('services/',views.services, name='services'),
    path('contact/',views.contact, name='contact'),
    path('feedback/',views.feedback, name='feedback'),
    path('user/',views.Login, name='login'),
    path('signup/',views.SignUp, name='signup'),
    path('logout/',views.LogoutPage,name='logout'),
    path('userProfile/',views.user_profile,name='profile'),
    path('editprofile/',views.change_profile,name='change_profile'),
    path('profile/',views.profile, name="MyuserProfile"),
    path('chat/', views.chatbot, name='chat'),
    path('changepassword/', views.change_password, name='change_password'),
    
]
