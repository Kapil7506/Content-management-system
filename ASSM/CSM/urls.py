from django.urls import path, include
from CSM.views import AuthorregistrationView, AuthorLoginView, Authorprofile, AuthorChangePasswordView, SendPasswordResetEmailView, AuthorpasswordResetView
urlpatterns = [
    path('register/', AuthorregistrationView.as_view(), name='register'),
    path('Login/', AuthorLoginView.as_view(), name='Login'),
    path('profile/', Authorprofile.as_view(), name= 'profile'),
    path('Changepassword/', AuthorChangePasswordView.as_view(), name='changepassword'),
    path('send-Resetpassword-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', AuthorpasswordResetView.as_view(), name='reset-password')
    ]
