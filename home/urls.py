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
<<<<<<< HEAD
    path('chat/', views.chatbot, name='chat')
    
=======
    path('profile/',views.profile, name="MyuserProfile")
>>>>>>> dd2c595c54982b9616578a755f1eb90fe1c0c6b9
]
