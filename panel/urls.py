from django.urls import path, include
import panel.views

urlpatterns = [
    path('', panel.views.root_handler),
    path('bookings/', panel.views.bookings_handler),
    path('specialist/', panel.views.specialist_handler),
    path('specialist/<int:specialist_id>/', panel.views.specialist_id_handler),
    path('specialist/<int:specialist_id>/schedule/', panel.views.specialist_schedule),
    path('services/', panel.views.services_handler),
    #path('services/<name_service>/', panel.views.service_id_handler),
]
