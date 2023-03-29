from django.urls import path, include
import user.views

urlpatterns = [
    path('', user.views.user_handler),
]