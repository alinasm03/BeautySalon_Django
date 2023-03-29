from django.urls import path, include
import services.views

urlpatterns = [
    path('services/', services.views.root_handler),
    path('services/<str:service_name>/', services.views.service_name_handler),
    path('specialist/', services.views.specialist_handler),
    path('specialist/<int:specialist_id>/', services.views.specialist_id_handler),
    path('booking/', services.views.booking_handler),
]
