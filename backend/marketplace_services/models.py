from django.db import models

from accounts.models import User


class Category(models.Model):
	name = models.CharField(max_length=100, unique=True)

	def __str__(self) -> str:
		return self.name


class Service(models.Model):
	freelancer = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='services',
		limit_choices_to={'role': User.Role.FREELANCER},
	)
	title = models.CharField(max_length=180)
	description = models.TextField()
	image = models.ImageField(upload_to='services/', blank=True, null=True)
	category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='services')
	price = models.DecimalField(max_digits=10, decimal_places=2)
	delivery_time = models.PositiveIntegerField(help_text='Estimated delivery time in days')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self) -> str:
		return self.title
