from django.urls import path, re_path
from . import views


app_name = 'photo_gallery'

urlpatterns = [
    path('gallery/', views.gallery, name='gallery'),
    path('upload-image/', views.upload_image, name='upload_image'),
    path('list-images/', views.list_images, name="list_images"),
    path('del-image/', views.del_image, name='del_image'),
]
