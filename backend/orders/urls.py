from django.urls import path

from .views import FreelancerReviewsView, OrderDetailView, OrderListCreateView, OrderReviewByOrderView, OrderStatusUpdateView

urlpatterns = [
    path('', OrderListCreateView.as_view(), name='orders-list-create'),
    path('<int:pk>/', OrderDetailView.as_view(), name='orders-detail'),
    path('<int:pk>/status/', OrderStatusUpdateView.as_view(), name='orders-status'),
    path('<int:order_id>/review/', OrderReviewByOrderView.as_view(), name='orders-review'),
    path('freelancer/<int:freelancer_id>/reviews/', FreelancerReviewsView.as_view(), name='freelancer-reviews'),
]
