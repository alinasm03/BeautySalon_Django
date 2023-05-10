from django.urls import path, include
import user.views

urlpatterns = [
    path('', user.views.user_handler),
    path('registration/', user.views.user_registration),
    path('login/', user.views.user_login),
    path('logout/', user.views.user_logout)
]
