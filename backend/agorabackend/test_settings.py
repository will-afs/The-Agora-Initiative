from django.template.defaultfilters import slugify
from django.urls import reverse

# VARIABLES
USERNAME_1 = 'uSername1'
PASSWORD_1 = '!password1'
EMAIL_1 = 'email1@gmail.com'

USERNAME_2 = 'uSername2'
PASSWORD_2 = '!password2'
EMAIL_2 = 'email2@gmail.com'

USERNAME_3 = 'uSername3'
PASSWORD_3 = '!password3'
EMAIL_3 = 'email3@gmail.com'

COMMUNITY_BIO_1 = 'Community bio n°1'
COMMUNITY_BIO_2 = 'Community bio n°2'

USER_PROFILE_BIO_1 = 'User profile bio n°1'
USER_PROFILE_BIO_2 = 'User profile bio n°2'


COMMUNITY_NAME_1 = 'CommunityNameExample1'
COMMUNITY_NAME_2 = 'CommunityNameExample2'

USER_PROFILE_SLUG_1 = slugify(USERNAME_1)
USER_PROFILE_SLUG_2 = slugify(USERNAME_2)

COMMUNITY_SLUG_1 = slugify(COMMUNITY_NAME_1)
COMMUNITY_SLUG_2 = slugify(COMMUNITY_NAME_2)

JOIN_REQUEST_PK_1 = '1'
JOIN_REQUEST_PK_2 = '2'

# DATA
REGISTRATION_DATA_1 = {
            'username': USERNAME_1,
            'password': PASSWORD_1,
            'email': EMAIL_1
        }
LOGIN_DATA_1 = {
    'username': USERNAME_1,
    'password': PASSWORD_1
    }
COMMUNITY_DATA_1 = {
            'name': COMMUNITY_NAME_1
        }
JOIN_REQUEST_DATA_1 = {
    'community name':COMMUNITY_NAME_1
} 

# URLS
REGISTRATION_URL = reverse('account_api:register')
LOGIN_URL = reverse('account_api:login')
USER_PROFILE_DETAIL_URL_1 = reverse(
                                        'userprofile_api:userprofile-detail',
                                        kwargs={'slug':USER_PROFILE_SLUG_1},
                                    )
USER_PROFILE_DETAIL_URL_2 = reverse(
                                        'userprofile_api:userprofile-detail',
                                        kwargs={'slug':USER_PROFILE_SLUG_2},
                                    )
USER_PROFILES_URL = reverse(
                                'userprofile_api:userprofile-list',
                            )
COMMUNITY_DETAIL_URL_1 = reverse(
                                    'community_api:community-detail',
                                    kwargs={'slug':COMMUNITY_SLUG_1},
                                )
COMMUNITY_DETAIL_URL_2 = reverse(
                                    'community_api:community-detail',
                                    kwargs={'slug':COMMUNITY_SLUG_2},
                                )
COMMUNITIES_URL = reverse('community_api:community-list')

JOIN_COMMUNITY_URL_1 = reverse(
                                    'community_api:community-join',
                                    kwargs={'slug':COMMUNITY_SLUG_1},
                                )
JOIN_COMMUNITY_URL_2 = reverse(
                                    'community_api:community-join',
                                    kwargs={'slug':COMMUNITY_SLUG_2},
                                )
JOIN_REQUESTS_URL_1 = reverse(
                                'community_api:join-request-list',
                                kwargs={'community_slug':COMMUNITY_SLUG_1}
                            )
JOIN_REQUESTS_URL_2 = reverse(
                                'community_api:join-request-list',
                                kwargs={'community_slug':COMMUNITY_SLUG_2}
                            )
JOIN_REQUEST_ACCEPT_URL_1 = reverse(
                                        'community_api:join-request-accept',
                                        kwargs={
                                                    'community_slug':COMMUNITY_SLUG_1,
                                                    'join_request_pk':JOIN_REQUEST_PK_1
                                                }
                                    )
JOIN_REQUEST_ACCEPT_URL_2 = reverse(
                                        'community_api:join-request-accept',
                                        kwargs={
                                                    'community_slug':COMMUNITY_SLUG_2,
                                                    'join_request_pk':JOIN_REQUEST_PK_2
                                                }
                                    )
JOIN_REQUEST_DECLINE_URL_1 = reverse(
                                        'community_api:join-request-decline',
                                        kwargs={
                                                    'community_slug':COMMUNITY_SLUG_1,
                                                    'join_request_pk':JOIN_REQUEST_PK_1
                                                }
                                    )
JOIN_REQUEST_DECLINE_URL_2 = reverse(
                                        'community_api:join-request-decline',
                                        kwargs={
                                                    'community_slug':COMMUNITY_SLUG_2,
                                                    'join_request_pk':JOIN_REQUEST_PK_2
                                                }
                                    )