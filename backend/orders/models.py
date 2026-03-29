from decimal import Decimal

from django.db import models
from django.db.models import Avg

from accounts.models import User
from marketplace_services.models import Service


class Order(models.Model):
	class Status(models.TextChoices):
		PENDING = 'pending', 'Pending'
		IN_PROGRESS = 'in_progress', 'In Progress'
		COMPLETED = 'completed', 'Completed'

	customer = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='customer_orders',
		limit_choices_to={'role': User.Role.CUSTOMER},
	)
	service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='orders')
	order_date = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
	dummy_payment_status = models.CharField(max_length=20, default='paid')

	class Meta:
		ordering = ['-order_date']


class Review(models.Model):
	order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='review')
	rating = models.PositiveSmallIntegerField()
	comment = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at']

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		freelancer = self.order.service.freelancer
		stats = Review.objects.filter(order__service__freelancer=freelancer).aggregate(avg=Avg('rating'))
		avg = stats['avg'] or 0
		freelancer.rating = Decimal(str(round(avg, 2)))
		freelancer.rating_count = Review.objects.filter(order__service__freelancer=freelancer).count()
		freelancer.save(update_fields=['rating', 'rating_count'])

# Create your models here.
