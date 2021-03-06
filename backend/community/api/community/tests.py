from community.api.community.serializers import CommunitySerializer
from django.test.testcases import TestCase
from community.models import Community, CommunityMember, JoinRequest
from rest_framework import status
from agorabackend.test_utils import APITestCaseWithAuth
from agorabackend import test_settings as conf
from account.models import Account


class CommunitySerializerTestCase(TestCase):
    def test_community_serializer_create_success(self):
        # Create a community serializer from community data
        data = conf.COMMUNITY_DATA_1
        community_serializer = CommunitySerializer(data=data)
        self.assertEqual(community_serializer.is_valid(), True)
        community_serializer.save()
        self.assertEqual(Community.objects.count(), 1)
        

    def test_community_serializer_partial_edit_success(self):
        community = Community(name=conf.COMMUNITY_NAME_1)
        community.save()
        self.assertEqual(Community.objects.filter(name=conf.COMMUNITY_NAME_1).count(), 1)
        data = {'bio':conf.COMMUNITY_BIO_2}
        community_serializer = CommunitySerializer(community, data=data, partial=True)
        self.assertEqual(community_serializer.is_valid(), True)
        community_serializer.save()
        self.assertEqual(Community.objects.filter(bio=data['bio']).count(), 1)


class CommunityCreateTestCase(APITestCaseWithAuth):
    
    def test_community_creation_without_auth_fails(self):
        response = self.client.post(conf.COMMUNITIES_URL, conf.COMMUNITY_DATA_1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Community.objects.count(), 0)

    def test_community_creation_with_correct_auth_success(self):
        self.authenticate()
        response = self.client.post(conf.COMMUNITIES_URL, conf.COMMUNITY_DATA_1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Community.objects.filter(name=conf.COMMUNITY_NAME_1).count(), 1)

    def test_community_creation_already_exists_fails(self):
        self.authenticate()
        self.client.post(conf.COMMUNITIES_URL, conf.COMMUNITY_DATA_1) # Community is created
        self.assertEqual(Community.objects.filter(name=conf.COMMUNITY_NAME_1).count(), 1)
        # Community creation attempt while it already exists
        response = self.client.post(conf.COMMUNITIES_URL, conf.COMMUNITY_DATA_1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Community.objects.filter(name=conf.COMMUNITY_NAME_1).count(), 1)

    def test_author_granted_as_admin_member_at_creation(self):
        self.authenticate()
        self.client.post(conf.COMMUNITIES_URL, conf.COMMUNITY_DATA_1) # Community is created
        self.assertEqual(CommunityMember.objects.count(), 1)
        self.assertEqual(CommunityMember.objects.get().is_admin, True)
        self.assertEqual(CommunityMember.objects.get().user.username, conf.USERNAME_1)

    def test_community_creation_with_incorrect_name_pattern_fails(self):
        self.authenticate()
        invalid_community_data = {
            'name': conf.COMMUNITY_NAME_1+'_',
        }
        response = self.client.post(conf.COMMUNITIES_URL, invalid_community_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Community.objects.count(), 0)


class CommunityEditTestCase(APITestCaseWithAuth):
    
    def test_community_edit_bio_as_admin_success(self):
        self.authenticate()
        # Create Community and grant user as an admin CommunityMember
        self.client.post(conf.COMMUNITIES_URL, conf.COMMUNITY_DATA_1)
        self.assertEqual(Community.objects.filter(slug=conf.COMMUNITY_SLUG_1).count(), 1)
        # Apply changes to Community bio field
        data = {'bio': 'New bio'}
        response = self.client.patch(conf.COMMUNITY_DETAIL_URL_1, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Community.objects.get(name = conf.COMMUNITY_NAME_1).bio, data['bio'])

    def test_community_edit_bio_as_simple_member_fails(self):
        account = self.authenticate()[0]
        # Create Community and grant user as a (not admin) CommunityMember
        community = Community(name=conf.COMMUNITY_NAME_1)
        community.save()
        community_member = CommunityMember(community=community, user=account)
        community_member.save()
        # Apply changes to Community bio field
        data = {'bio': 'New bio'}
        response = self.client.patch(conf.COMMUNITY_DETAIL_URL_1, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(Community.objects.get(name = conf.COMMUNITY_NAME_1).bio, data['bio'])

    def test_community_edit_no_auth_fails(self):
        community = Community(name=conf.COMMUNITY_NAME_1)
        community.save()
        # Apply changes to Community bio field
        data = {'bio': 'New bio'}
        response = self.client.patch(conf.COMMUNITY_DETAIL_URL_1, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotEqual(Community.objects.get(name = conf.COMMUNITY_NAME_1).bio, data['bio'])
    
class CommunityGetTestCase(APITestCaseWithAuth):
    
    def test_get_community_no_auth_fails(self):
        community = Community(name=conf.COMMUNITY_NAME_1)
        community.save()
        response = self.client.get(conf.COMMUNITY_DETAIL_URL_1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_community_being_member_success(self):
        self.authenticate()
        # Create Community and grant user as an admin CommunityMember
        self.client.post(conf.COMMUNITIES_URL, conf.COMMUNITY_DATA_1)
        community = Community.objects.get(name=conf.COMMUNITY_NAME_1)
        community_serializer = CommunitySerializer(community)
        response = self.client.get(conf.COMMUNITY_DETAIL_URL_1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, community_serializer.data)
        
    def test_get_community_not_being_member_fails(self):
        self.authenticate()
        # Create a Community without any member
        community = Community(name=conf.COMMUNITY_NAME_1)
        community.save()
        self.assertEqual(Community.objects.filter(name=conf.COMMUNITY_NAME_1).count(), 1)
        response = self.client.get(conf.COMMUNITY_DETAIL_URL_1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        

class CommunityGetListTestCase(APITestCaseWithAuth):
    
    def test_get_list_community_success(self):
        self.authenticate()
        # Test with an empty Community table
        response = self.client.get(conf.COMMUNITIES_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

        # Populate the Community table with two instances
        community_1 = Community(name=conf.COMMUNITY_NAME_1)
        community_2 = Community(name=conf.COMMUNITY_NAME_2)
        community_1.save()
        community_2.save()

        response = self.client.get(conf.COMMUNITIES_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], conf.COMMUNITY_NAME_1)
        self.assertEqual(response.data[1]['name'], conf.COMMUNITY_NAME_2)

