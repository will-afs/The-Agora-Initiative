from django.template.defaultfilters import slugify
from django.urls import reverse

# VARIABLES
USERNAME = 'testcase'
PASSWORD = 'somestrongPassword'
EMAIL = 'testcase@gmail.com'
BIO = 'Dummy bio 990097'
COMMUNITY_NAME = 'CommunityNameExample'
USER_PROFILE_SLUG = slugify(USERNAME)
COMMUNITY_SLUG = slugify(COMMUNITY_NAME)

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
COMMUNITY_DATA = {
            'name': COMMUNITY_NAME
        }
JOIN_REQUEST_DATA = {
    'community name':COMMUNITY_NAME
} 

# URLS
REGISTRATION_URL = reverse('account_api:register')
LOGIN_URL = reverse('account_api:login')
USER_PROFILE_DETAIL_URL = reverse(
                                'userprofile_api:userprofile-detail',
                                kwargs={'slug':USER_PROFILE_SLUG},
                                )
USER_PROFILES_URL = reverse(
                                'userprofile_api:userprofile-list',
                                )
COMMUNITY_DETAIL_URL = reverse(
                            'community_api:community-detail',
                            kwargs={'slug':COMMUNITY_SLUG},
                        )
COMMUNITIES_URL = reverse('community_api:community-list')

JOIN_COMMUNITY_URL = reverse(
                                'community_api:community-join',
                                kwargs={'slug':COMMUNITY_SLUG},
                                )