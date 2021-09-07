from django.db import models
from account.models import Account
from django.template.defaultfilters import slugify


class UserProfile(models.Model):
    account = models.OneToOneField(
            Account,
            on_delete=models.CASCADE,
            null=True,
            unique=True
        )
    slug = models.SlugField(max_length=30, blank=True, default = slugify(account), unique=True)
    bio = models.CharField(max_length=150, blank=True, default='')

    # Future fields
    # -------------
    # picture = models.ImageField(upload_to='cars')
    # influence_points = models.PositiveIntegerField()
    # trophies : list of trophies objects
    # honorific_title = choice among available honorific titles
    # activity : 
    # followers : list of users following the current user
    # follows : list users the current follows
    # communities : list of communities of which user belongs
    # certified_info : (name, surname, birth_date, gender, etc.)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.account.username)
        super(UserProfile, self).save(*args, **kwargs)

    
    def __str__(self):
        return self.user_account.get_username()