from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
	model = User
	list_display = ('id', 'email', 'name', 'role', 'rating')
	fieldsets = UserAdmin.fieldsets + (
		('Marketplace Info', {'fields': ('name', 'role', 'bio', 'skills', 'rating', 'rating_count')}),
	)
