from django.urls import path
from django.contrib.auth import views as auth_views
from .views import request_password_reset, confirm_reset_password
from .views import CustomPasswordResetConfirmView 
from . import views

urlpatterns = [
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='reset_password.html',
             email_template_name='password_reset_email.html',
             success_url='/password-reset/done/'
         ), name='password_reset'),
    
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='password_reset_done.html'
         ), name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/',
         CustomPasswordResetConfirmView.as_view( 
             template_name='password_reset_confirm.html',
             success_url='/reset/done/'
         ), name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password_reset_complete.html'
         ), name='password_reset_complete'),         
]