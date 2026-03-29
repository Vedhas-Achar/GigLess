from django.urls import path

from .views import CategoryListView, ServiceDetailView, ServiceListCreateView

urlpatterns = [
    path('', ServiceListCreateView.as_view(), name='service-list-create'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('<int:pk>/', ServiceDetailView.as_view(), name='service-detail'),
]
