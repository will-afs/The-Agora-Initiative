from django.template.defaultfilters import slugify
from django.urls import reverse

# VARIABLES
USERNAME = 'testcase'
PASSWORD = 'somestrongPassword'
EMAIL = 'testcase@gmail.com'
BIO = 'Dummy bio 990097'
USER_PROFILE_SLUG = slugify(USERNAME)

# DATA
REGISTRATION_DATA = {
            'username': USERNAME,
            'password': PASSWORD,
            'email': EMAIL
        }
LOGIN_DATA = {
    'username': USERNAME,
    'password': PASSWORD
    }

# URLS
REGISTRATION_URL = reverse('account_api:register')
LOGIN_URL = reverse('account_api:login')
USER_PROFILE_DETAIL_URL = reverse(
                                'userprofile_api:userprofile-detail',
                                kwargs={'slug':USER_PROFILE_SLUG},
                                # kwargs={'userprofile_slug':user_profile_slug},
                                )
USER_PROFILES_URL = reverse(
                                'userprofile_api:userprofile-list',
                                )