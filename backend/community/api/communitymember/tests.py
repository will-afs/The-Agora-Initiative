from rest_framework.exceptions import ValidationError
from account.api.serializers import AccountSerializer
from community.api.community.serializers import CommunitySerializer
from community.api.communitymember.serializers import CommunityMemberSerializer
from django.test.testcases import TestCase
from community.models import Community, CommunityMember
from account.models import Account
from agorabackend.test_utils import register
from agorabackend import test_settings as conf

        
class CommunityMemberSerializerTestCase(TestCase):
    def setUp(self):
        self.account = register()
        self.assertEqual(Account.objects.count(), 1)
        self.community = Community(name = conf.COMMUNITY_NAME_1)
        self.community.save()
        self.assertEqual(Community.objects.count(), 1)

    def test_community_member_create_success(self):
        data={'user':self.account.pk, 'community':self.community.pk, 'is_admin':False}
        community_member_serializer = CommunityMemberSerializer(data=data)
        self.assertEqual(community_member_serializer.is_valid(), True)
        community_member_serializer.save()
        self.assertEqual(CommunityMember.objects.count(), 1)

    def test_community_member_serializer_partial_edit_admin_success(self):
        community_member = CommunityMember(user=self.account, community=self.community, is_admin=False)
        community_member.save()
        self.assertEqual(CommunityMember.objects.count(), 1)
        self.assertEqual(community_member.is_admin, False)
        data={'is_admin':True}
        community_member_serializer = CommunityMemberSerializer(community_member, data=data, partial=True)
        self.assertEqual(community_member_serializer.is_valid(), True)
        community_member_serializer.save()
        self.assertEqual(community_member.is_admin, True)

    def test_community_member_serializer_partial_edit_community_fails(self):
        community_member = CommunityMember(user=self.account, community=self.community, is_admin=False)
        community_member.save()
        self.assertEqual(CommunityMember.objects.count(), 1)
        self.assertEqual(community_member.user, self.account)
        community_2 = Community(name=conf.COMMUNITY_NAME_2)
        community_2.save()
        data = {'community':community_2.pk}
        community_member_serializer = CommunityMemberSerializer(community_member, data=data, partial=True)
        self.assertEqual(community_member_serializer.is_valid(), True)
        community_member_serializer.save()
        self.assertEqual(community_member.community, self.community)

    def test_community_member_serializer_get_success(self):
        community_member = CommunityMember(user=self.account, community=self.community, is_admin=False)
        community_member.save()
        self.assertEqual(CommunityMember.objects.count(), 1)
        community_member_serializer = CommunityMemberSerializer(community_member)
        account_serializer = AccountSerializer(self.account)
        community_serializer = CommunitySerializer(self.community)
        self.assertEqual(community_member_serializer.data['user'], account_serializer.data)
        self.assertEqual(community_member_serializer.data['community'], community_serializer.data)
        self.assertEqual(community_member_serializer.data['is_admin'], False)

    def test_community_member_already_exists_fails(self):
        community_member = CommunityMember(user=self.account, community=self.community, is_admin=False)
        community_member.save()
        self.assertEqual(CommunityMember.objects.count(), 1)
        data={'user':self.account.pk, 'community':self.community.pk, 'is_admin':True}
        community_member_serializer = CommunityMemberSerializer(data=data)
        with self.assertRaises(ValidationError):
            community_member_serializer.is_valid(raise_exception=True)
        self.assertEqual(CommunityMember.objects.count(), 1)