from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
	class Role(models.TextChoices):
		FREELANCER = 'freelancer', 'Freelancer'
		CUSTOMER = 'customer', 'Customer'

	name = models.CharField(max_length=120)
	email = models.EmailField(unique=True)
	role = models.CharField(max_length=20, choices=Role.choices)
	bio = models.TextField(blank=True)
	skills = models.TextField(blank=True)
	profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
	rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
	rating_count = models.PositiveIntegerField(default=0)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username', 'name', 'role']

	def __str__(self) -> str:
		return f"{self.name} ({self.email})"
