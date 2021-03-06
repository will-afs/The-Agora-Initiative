from rest_framework.exceptions import ErrorDetail, ValidationError
from account.api.serializers import AccountSerializer
from community.api.community.serializers import CommunitySerializer
from community.api.joinrequest.serializers import JoinRequestSerializer
from django.test.testcases import TestCase
from community.models import Community, CommunityMember, JoinRequest
from account.models import Account
from rest_framework import status
from agorabackend.test_utils import APITestCaseWithAuth, register
from agorabackend import test_settings as conf


class JoinRequestSerializerTestCase(TestCase):

    def setUp(self):
        self.account = register()
        self.assertEqual(Account.objects.count(), 1)
        self.community = Community(name = conf.COMMUNITY_NAME_1)
        self.community.save()
        self.assertEqual(Community.objects.count(), 1)

    def test_join_request_serializer_create_success(self):
        data={'user':self.account.pk, 'community':self.community.pk}
        join_request_serializer = JoinRequestSerializer(data=data)
        self.assertEqual(join_request_serializer.is_valid(), True)
        join_request_serializer.save()
        self.assertEqual(JoinRequest.objects.count(), 1)

    def test_join_request_serializer_partial_edit_fails(self):
        join_request = JoinRequest(user=self.account, community=self.community)
        join_request.save()
        self.assertEqual(JoinRequest.objects.count(), 1)
        self.assertEqual(join_request.community, self.community)
        community_2 = Community(name=conf.COMMUNITY_NAME_2)
        community_2.save()
        data = {'community':community_2.pk}
        join_request_serializer = JoinRequestSerializer(join_request, data=data, partial=True)
        self.assertEqual(join_request_serializer.is_valid(), True)
        join_request_serializer.save()
        self.assertEqual(join_request.community, self.community)

    def test_join_request_serializer_get_success(self):
        join_request = JoinRequest(user=self.account, community=self.community)
        join_request.save()
        self.assertEqual(JoinRequest.objects.count(), 1)
        join_request_serializer = JoinRequestSerializer(join_request)
        account_serializer = AccountSerializer(self.account)
        community_serializer = CommunitySerializer(self.community)
        self.assertEqual(join_request_serializer.data['user'], account_serializer.data)
        self.assertEqual(join_request_serializer.data['community'], community_serializer.data)

    def test_join_request_but_community_member_already_exists_fails(self):
        community_member = CommunityMember(user=self.account, community=self.community, is_admin=False)
        community_member.save()
        self.assertEqual(CommunityMember.objects.count(), 1)
        data={'user':self.account.pk, 'community':self.community.pk}
        join_request_serializer = JoinRequestSerializer(data=data)
        with self.assertRaises(ValidationError):
            join_request_serializer.is_valid(raise_exception=True)   

    def test_join_request_but_one_already_exists_fails(self):
        join_request = JoinRequest(user=self.account, community=self.community)
        join_request.save()
        self.assertEqual(JoinRequest.objects.count(), 1)        
        data={'user':self.account.pk, 'community':self.community.pk}
        join_request_serializer = JoinRequestSerializer(data=data)
        with self.assertRaises(ValidationError):
            join_request_serializer.is_valid(raise_exception=True)


class JoinTestCase(APITestCaseWithAuth):
    
    def test_create_join_request_success(self):
        # Create an account and Log in
        account = self.authenticate()[0]
        # Create community
        community = Community(name=conf.COMMUNITY_NAME_1)
        community.save()
        self.assertEqual(Community.objects.count(), 1)
        # Ask to join the community
        response = self.client.post(conf.JOIN_COMMUNITY_URL_1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(JoinRequest.objects.filter(user=account, community=community).count(), 1)

    def test_create_join_request_no_auth_fails(self):
        # Create community
        community = Community(name=conf.COMMUNITY_NAME_1)
        community.save()
        # Ask to join the community
        response = self.client.post(conf.JOIN_COMMUNITY_URL_1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)    
        self.assertEqual(JoinRequest.objects.count(), 0)

    def test_create_join_request_community_does_not_exist_fails(self):
        # Create an account and Log in
        self.authenticate() 
        # Ask to join the community
        response = self.client.post(conf.JOIN_COMMUNITY_URL_1)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)    
        self.assertEqual(JoinRequest.objects.count(), 0)

    def test_create_join_request_already_exists_fails(self):
        # Create an account and Log in
        self.authenticate()
        account = Account.objects.get(username=conf.USERNAME_1)
        # Create community
        community = Community(name=conf.COMMUNITY_NAME_1)
        community.save()
        # Create a first join request on this community for this user
        join_request = JoinRequest(community=community, user=account)
        join_request.save()
        # Attempt to create a new one
        response = self.client.post(conf.JOIN_COMMUNITY_URL_1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(JoinRequest.objects.count(), 1)

    def test_create_join_request_but_already_member_fails(self):
        # Create an account and Log in
        account = self.authenticate()[0]
        # Create community
        community = Community(name=conf.COMMUNITY_NAME_1)
        community.save()
        # Create a first join request on this community for this user
        community_member = CommunityMember(community=community, user=account)
        community_member.save()
        # Attempt to create a join request but user is already a member of community
        response = self.client.post(conf.JOIN_COMMUNITY_URL_1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)    
        self.assertEqual(JoinRequest.objects.count(), 0)


class JoinRequestViewTestCase(APITestCaseWithAuth):
    def setUp(self):
        self.community = Community(name=conf.COMMUNITY_NAME_1)
        self.community.save()
        self.community_2 = Community(name=conf.COMMUNITY_NAME_2)
        self.community_2.save()
        # self.account = register()

    def test_get_list_join_request_as_admin_success(self):
        # Log in with a community admin account
        account = self.authenticate()[0]
        community_member = CommunityMember(user = account, community=self.community, is_admin=True)
        community_member.save()

        # Test with an empty JoinRequests table
        response = self.client.get(conf.JOIN_REQUESTS_URL_1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

        account_2 = register(username=conf.USERNAME_2, password=conf.PASSWORD_2, email=conf.EMAIL_2)
        # Populate the JoinRequests table with two instances of different communities
        join_request_1 = JoinRequest(user=account_2, community=self.community)
        join_request_2 = JoinRequest(user=account, community=self.community_2)
        join_request_1.save()
        join_request_2.save()

        # Lookup join requests concerning community (not community_2)
        response = self.client.get(conf.JOIN_REQUESTS_URL_1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0], JoinRequestSerializer(join_request_1).data)

        # Add a new join request to community (not community_2)
        account_3 = register(username=conf.USERNAME_3, password=conf.PASSWORD_3, email=conf.EMAIL_3)
        join_request_3 = JoinRequest(user=account_3, community=self.community)
        join_request_3.save()
        response = self.client.get(conf.JOIN_REQUESTS_URL_1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0], JoinRequestSerializer(join_request_1).data)
        self.assertEqual(response.data[1], JoinRequestSerializer(join_request_3).data)

    def test_get_list_join_request_not_admin_fails(self):
        # Log in with a non admin account
        account = self.authenticate()[0]
        # Test with an empty JoinRequests table
        response = self.client.get(conf.JOIN_REQUESTS_URL_1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(type(response.data['detail']), ErrorDetail)

    def test_join_request_list_not_authenticated_fails(self):
        account = register()

        # Create a join request
        join_request_1 = JoinRequest(user=account, community=self.community)
        join_request_1.save()
        self.assertEqual(JoinRequest.objects.filter(pk=join_request_1.pk).count(), 1)

        # Send the request
        response = self.client.get(conf.JOIN_REQUESTS_URL_1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(type(response.data['detail']), ErrorDetail)

    def test_join_request_accept_as_admin_success(self):
        account = self.authenticate()[0]
        community_member = CommunityMember(user = account, community=self.community, is_admin=True)
        community_member.save()
        account_2 = register(username=conf.USERNAME_2, password=conf.PASSWORD_2, email=conf.EMAIL_2)
        # Create a join request
        join_request_1 = JoinRequest(user=account_2, community=self.community)
        join_request_1.save()
        self.assertEqual(JoinRequest.objects.filter(pk=join_request_1.pk).count(), 1)

        # Send the request
        response = self.client.delete(conf.JOIN_REQUEST_ACCEPT_URL_1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Ensure the user related to the join request has been added as a member of the community
        self.assertEqual(CommunityMember.objects.filter(user=account, community=self.community).count(), 1)
        # Ensure the join request has been deleted
        self.assertEqual(JoinRequest.objects.filter(pk=join_request_1.pk).count(), 0)

    def test_join_request_accept_not_admin_fails(self):
        account = self.authenticate()
        # Create a join request
        join_request_1 = JoinRequest(user=account[0], community=self.community)
        join_request_1.save()
        self.assertEqual(JoinRequest.objects.filter(pk=join_request_1.pk).count(), 1)

        # Send the request
        response = self.client.delete(conf.JOIN_REQUEST_ACCEPT_URL_1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(type(response.data['detail']), ErrorDetail)

        # Ensure the join request has not been deleted
        self.assertEqual(JoinRequest.objects.filter(pk=join_request_1.pk).count(), 1)

    def test_join_request_accept_not_authenticated_fails(self):
        account = register()

        # Create a join request
        join_request_1 = JoinRequest(user=account, community=self.community)
        join_request_1.save()
        self.assertEqual(JoinRequest.objects.filter(pk=join_request_1.pk).count(), 1)

        # Send the request
        response = self.client.delete(conf.JOIN_REQUEST_ACCEPT_URL_1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(type(response.data['detail']), ErrorDetail)

        # Ensure the join request has not been deleted
        self.assertEqual(JoinRequest.objects.filter(pk=join_request_1.pk).count(), 1)

    def test_join_request_decline_as_admin_success(self):
        account = self.authenticate()[0]
        community_member = CommunityMember(user = account, community=self.community, is_admin=True)
        community_member.save()

        # Create a join request
        account_2 = register(username=conf.USERNAME_2, password=conf.PASSWORD_2, email=conf.EMAIL_2)
        join_request_1 = JoinRequest(user=account_2, community=self.community)
        join_request_1.save()
        self.assertEqual(JoinRequest.objects.filter(pk=join_request_1.pk).count(), 1)

        # Send the request
        response = self.client.delete(conf.JOIN_REQUEST_DECLINE_URL_1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Ensure the join request has been deleted
        self.assertEqual(JoinRequest.objects.filter(pk=join_request_1.pk).count(), 0)

    def test_join_request_decline_not_admin_fails(self):
        account = self.authenticate()[0]

        # Create a join request
        join_request_1 = JoinRequest(user=account, community=self.community)
        join_request_1.save()
        self.assertEqual(JoinRequest.objects.filter(pk=join_request_1.pk).count(), 1)

        # Send the request
        response = self.client.delete(conf.JOIN_REQUEST_DECLINE_URL_1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(type(response.data['detail']), ErrorDetail)

        # Ensure the join request has not been deleted
        self.assertEqual(JoinRequest.objects.filter(pk=join_request_1.pk).count(), 1)

    def test_join_request_decline_not_authenticated_fails(self):
        account = register()

        # Create a join request
        join_request_1 = JoinRequest(user=account, community=self.community)
        join_request_1.save()
        self.assertEqual(JoinRequest.objects.filter(pk=join_request_1.pk).count(), 1)

        # Send the request
        response = self.client.delete(conf.JOIN_REQUEST_DECLINE_URL_1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(type(response.data['detail']), ErrorDetail)

        # Ensure the join request has not been deleted
        self.assertEqual(JoinRequest.objects.filter(pk=join_request_1.pk).count(), 1)