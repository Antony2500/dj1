from django.urls import path

from .views import ItemsView

urlpatterns = [
    path("items", ItemsView.as_view(), name='items')
]
