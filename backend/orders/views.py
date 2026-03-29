from django.db.models import Q
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Order, Review
from .permissions import IsOrderParticipant
from .serializers import OrderSerializer, OrderStatusSerializer, ReviewSerializer


class OrderListCreateView(generics.ListCreateAPIView):
	serializer_class = OrderSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		return (
            Order.objects.select_related('service', 'service__freelancer', 'customer')
			.filter(Q(service__freelancer=user) | Q(customer=user))
			.distinct()
		)


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrderParticipant]
    queryset = Order.objects.select_related('service', 'service__freelancer', 'customer').all()


class OrderStatusUpdateView(generics.UpdateAPIView):
    serializer_class = OrderStatusSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrderParticipant]
    queryset = Order.objects.select_related('service').all()

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        new_status = request.data.get('status')
        user = request.user

        if new_status == Order.Status.IN_PROGRESS and user.id != order.service.freelancer_id:
            return Response({'detail': 'Only freelancer can move order to in progress.'}, status=status.HTTP_403_FORBIDDEN)
        if new_status == Order.Status.COMPLETED and user.id != order.customer_id:
            return Response({'detail': 'Only customer can complete order.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(order, data={'status': new_status}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(OrderSerializer(order).data)


class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]


class OrderReviewByOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, order_id):
        payload = {
            'order': order_id,
            'rating': request.data.get('rating'),
            'comment': request.data.get('comment', ''),
        }
        serializer = ReviewSerializer(data=payload, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FreelancerReviewsView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        freelancer_id = self.kwargs['freelancer_id']
        return Review.objects.select_related('order', 'order__service').filter(order__service__freelancer_id=freelancer_id)
