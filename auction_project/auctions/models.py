from django.db import models

from .enums import StatusEnum

from accounts.models import Profile


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'


class Auction(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    initial_price = models.PositiveIntegerField()
    current_price = models.PositiveIntegerField()
    number_of_bids = models.PositiveIntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)
    days_to_end = models.PositiveIntegerField(default=2)
    step = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=50, choices=[
                              (s.name, s.value) for s in StatusEnum],
                              default='Open')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 blank=True, null=True)
    owner = models.ForeignKey(Profile,
                              on_delete=models.CASCADE,
                              related_name='auction_owner')
    winner = models.ForeignKey(Profile,
                               on_delete=models.CASCADE,
                               related_name='auction_winer',
                               blank=True, null=True)
    participants = models.ManyToManyField('accounts.Profile',
                                          related_name='auction_participants',
                                          blank=True)

    def __str__(self):
        return f'Auction title - {self.title} with owner - {self.owner}'
