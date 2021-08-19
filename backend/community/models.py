from django.db import models
from account.models import Account
from django.template.defaultfilters import slugify
# Create your models here.

class Community(models.Model):
    name = models.CharField(max_length=30, unique=True)
    bio = models.CharField(max_length=150, blank=True)
    slug = models.SlugField(max_length=30, blank=True)

    
    # picture = models.ImageField()
    # posts = 
    # admins = models.ManyToManyField(Account, on_delete=models.DO_NOTHING, blank=False)
    class Meta(object):
        verbose_name_plural = 'Communities'
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Community, self).save(*args, **kwargs)

class CommunityMember(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, blank=False)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, blank=False)
    is_admin = models.BooleanField(default=False)


class JoinRequest(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, blank=False)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, blank=False)
    creation_date = models.DateTimeField(auto_now_add=True, blank=False)

