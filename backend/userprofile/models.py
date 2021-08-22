from django.db import models

class UserProfile(models.Model):
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

    def __str__(self):
        return self.user_account.get_username()