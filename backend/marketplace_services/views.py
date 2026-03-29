from django.db.models import Q
from rest_framework import filters, generics, permissions

from .models import Category, Service
from .permissions import IsOwnerFreelancerOrReadOnly
from .serializers import CategorySerializer, ServiceSerializer


class CategoryListView(generics.ListCreateAPIView):
	queryset = Category.objects.all().order_by('name')
	serializer_class = CategorySerializer

	def get_permissions(self):
		if self.request.method == 'GET':
			return [permissions.AllowAny()]
		return [permissions.IsAuthenticated()]


class ServiceListCreateView(generics.ListCreateAPIView):
	serializer_class = ServiceSerializer
	permission_classes = [IsOwnerFreelancerOrReadOnly]
	filter_backends = [filters.OrderingFilter]
	ordering_fields = ['price', 'created_at']
	ordering = ['-created_at']

	def get_queryset(self):
		queryset = Service.objects.select_related('freelancer', 'category').all()
		keyword = self.request.query_params.get('keyword')
		category = self.request.query_params.get('category')
		price_min = self.request.query_params.get('price_min')
		price_max = self.request.query_params.get('price_max')
		rating_min = self.request.query_params.get('rating_min')

		if keyword:
			queryset = queryset.filter(Q(title__icontains=keyword) | Q(description__icontains=keyword))
		if category:
			queryset = queryset.filter(
				Q(category_id=category) | Q(category__name__iexact=category)
			)
		if price_min:
			queryset = queryset.filter(price__gte=price_min)
		if price_max:
			queryset = queryset.filter(price__lte=price_max)
		if rating_min:
			queryset = queryset.filter(freelancer__rating__gte=rating_min)
		return queryset


class ServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = Service.objects.select_related('freelancer', 'category').all()
	serializer_class = ServiceSerializer
	permission_classes = [IsOwnerFreelancerOrReadOnly]
