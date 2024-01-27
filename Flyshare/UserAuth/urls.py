from django.urls import path
from .views import *
from . import views
from .Password import *
from .forms import UserPasswordResetForm
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('auth/',UserModelAPI.as_view()),
    path('auth/<int:id>/',UserModelAPI_ID.as_view()),
    path('',views.indexPage,name='index'),
    path('verify/',views.verifyPage,name='verify'),
    path('register/', views.registerPage, name='register'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('login/',views.loginPage,name='login'),
    path('base/',views.basePage,name='base'),
    path('submit/', views.submit_form, name='submit_form'),
    path('logout/', views.logout_view, name='logout'),
    # path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('profile/', views.profilePage, name='profile'),
    path('edit_profile/', views.edit_profilePage, name='edit_profile'),
    path('change/', views.change_passwordPage, name='change_password_page'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
    template_name='Login/password_reset_form.html',
    email_template_name = 'Login/password_reset_email.html',
    subject_template_name = 'Login/password_reset_subject.txt',
    success_url = '/password_reset_done/',
    form_class=UserPasswordResetForm),name='password_reset'),
]
