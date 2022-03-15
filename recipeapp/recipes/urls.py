from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('recipe/<int:recipe_id>', views.recipe_details, name='recipe_details'),
]
urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)