from django.test import TestCase
from django.db import IntegrityError
from agorabackend.test_utils import register 
from agorabackend import test_settings as conf
from community.models import Community, CommunityMember, JoinRequest

# Create your tests here.

class JoinTestCase(TestCase):        

    def test_create_join_request_but_one_already_exists_fails(self):
        # Create an account and Log on
        account = register()
        # Create community
        community = Community(name=conf.COMMUNITY_NAME)
        community.save()
        # Create a first join request on this community for this user
        join_request = JoinRequest(community=community, user=account)
        join_request.save()
        self.assertEqual(JoinRequest.objects.filter(user=account, community=community).count(), 1)
        # Create a second join request on this community for this user
        with self.assertRaises(IntegrityError):
            join_request = JoinRequest(community=community, user=account)
            join_request.save()
            self.assertEqual(JoinRequest.objects.filter(user=account, community=community).count(), 1)

class CommunityMemberCreateTestCase(TestCase):        

    def test_join_request_deleted_at_community_member_creation_success(self):
        account = register()
        community = Community(name=conf.COMMUNITY_NAME)
        community.save()
        # Create a first join request on this community for this user
        join_request = JoinRequest(community=community, user=account)
        join_request.save()
        self.assertEqual(JoinRequest.objects.count(), 1)
        community_member = CommunityMember(community=community, user=account)
        community_member.save()
        self.assertEqual(CommunityMember.objects.count(), 1)
        self.assertEqual(JoinRequest.objects.count(), 0)
