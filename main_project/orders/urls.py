from django.urls import path
from . import views


urlpatterns = [
    # React API Endpoints
    path('api/comments/', views.comments_api, name='comments_api'),
    path('api/contact/', views.contact_api, name='contact_api'),
  path('send_email_to_client/<int:order_id>/', views.send_email_to_client, name='send_email_to_client'),
    path('api/contact-page/<int:order_id>/', views.contact_page_api, name='contact_page_api'),
    path('api/index/', views.index_api, name='index_api'),
     path('api/about/', views.about_api, name='about_api'),
    path('api/gallery/', views.gallery_api, name='gallery_api'),
    path('api/bathrooms/', views.bathrooms_api, name='bathrooms_api'),
    path('api/kitchens/', views.kitchens_api, name='kitchens_api'),
    path('api/fireplaces/', views.fireplaces_api, name='fireplaces_api'),
    
]
