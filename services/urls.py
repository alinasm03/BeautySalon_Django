from django.urls import path, include
import services.views

urlpatterns = [
    path('services/', services.views.service_handler),
    path('services/<int:service_id>/', services.views.service_name_handler),
    path('specialist/', services.views.specialist_handler),
    path('specialist/<int:specialist_id>/', services.views.specialist_id_handler),
]
