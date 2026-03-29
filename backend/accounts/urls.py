from django.urls import path

from .views import LoginView, LogoutView, MeView, PublicFreelancerProfileView, RefreshTokenView, RegisterView

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh/', RefreshTokenView.as_view(), name='refresh'),
    path('me/', MeView.as_view(), name='me'),
    path('freelancers/<int:pk>/', PublicFreelancerProfileView.as_view(), name='freelancer-profile'),
]
