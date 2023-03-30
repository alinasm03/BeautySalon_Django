from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include("services.urls")),
    path('panel/', include("panel.urls")),
    path('user/', include("user.urls")),
    path('admin/', admin.site.urls),
]
