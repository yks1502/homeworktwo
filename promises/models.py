from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class Promise(models.Model):
  created = models.DateTimeField(auto_now_add=True)
  sinceWhen = models.DateTimeField()
  tilWhen = models.DateTimeField()
  user1 = models.ForeignKey(User, related_name='promises_as_inviter', on_delete=models.CASCADE)
  user2 = models.ForeignKey(User, related_name='promises_as_invitee', on_delete=models.CASCADE)

  class Meta:
    ordering = ('created',)

  def save(self, *args, **kwargs):
    super(Promise, self).save(*args, **kwargs)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)