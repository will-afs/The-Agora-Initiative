from django.db import models
from account.models import Account
from django.template.defaultfilters import slugify
from django.core.validators import RegexValidator

# Create your models here.

class Community(models.Model):
    name = models.CharField(
        max_length=30,
        unique=True,
        validators = [
                        RegexValidator(
                                        regex='^[a-zA-Z0-9]*$',
                                        message='Community name must be Alphanumeric.',
                                        code='invalid_username'
                            )
                    ]
    )
    bio = models.CharField(max_length=150, blank=True, default='')
    slug = models.SlugField(max_length=30, blank=True, default=slugify(name))

    class Meta(object):
        verbose_name_plural = 'Communities'
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Community, self).save(*args, **kwargs)

class CommunityMember(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    is_admin = models.BooleanField(blank=True, default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['community', 'user'], name='unique_communitymember')
        ]


class JoinRequest(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, editable=False)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, editable=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['community', 'user'], name='unique_joinrequest')
        ]

