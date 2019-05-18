from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save

from .enums import Languages


user_img = 'https://www.compassdigitalskills.eu/img/generic/generic-user.png'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='profile')
    # username = models.CharField(max_length=150, unique=True)
    profile_image = models.URLField(default=user_img)
    language = models.CharField(max_length=50,
                                choices=[(l.name, l.value) for l in Languages])
    created_at = models.DateField(auto_now_add=True)

    """
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
    """

    def delete(self, *args, **kwargs):
        self.user.delete()
        return super(self.__class__, self).delete(*args, **kwargs)

    def __str__(self):
        return f'{self.user}'
