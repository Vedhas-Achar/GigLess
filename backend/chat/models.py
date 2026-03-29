from django.db import models

from accounts.models import User
from orders.models import Order


class Conversation(models.Model):
	user_one = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations_started')
	user_two = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations_received')
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, related_name='conversations')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		constraints = [
			models.UniqueConstraint(fields=['user_one', 'user_two', 'order'], name='uniq_conversation_pair_order')
		]
		ordering = ['-updated_at']

	def save(self, *args, **kwargs):
		if self.user_one_id and self.user_two_id and self.user_one_id > self.user_two_id:
			self.user_one_id, self.user_two_id = self.user_two_id, self.user_one_id
		super().save(*args, **kwargs)


class Message(models.Model):
	conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
	sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
	content = models.TextField()
	is_read = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['created_at']
