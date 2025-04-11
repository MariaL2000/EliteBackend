# urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('comments/', views.comments, name='comments'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('gallery/', views.gallery, name='gallery'),
    path('send_email/<int:order_id>/', views.send_email_to_client, name='send_email_to_client'),
    path('bathrooms/', views.bathrooms, name='bathrooms'),
    path('kitchens/', views.kitchens, name='kitchens'),
    path('fireplaces/', views.fireplaces, name='fireplaces'),
    # Ruta para la página de contacto donde el cliente puede aceptar o rechazar la oferta
    path('contact_page/<int:order_id>/', views.contact_page, name='contact_page'),
]
