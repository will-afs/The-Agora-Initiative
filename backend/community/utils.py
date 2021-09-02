from account.models import Account
from community.models import Community, CommunityMember, JoinRequest

def is_community_admin(user:Account, community:Community)->bool:
    try:
        community_member = CommunityMember.objects.get(community=community, user=user)
        return community_member.is_admin
    except CommunityMember.DoesNotExist:
        return False

def community_member_exists(user:Account, community:Community)->bool:
    try:
        CommunityMember.objects.get(community=community, user=user)
        return True
    except CommunityMember.DoesNotExist:
        return False

def join_request_exists(user:Account, community:Community)->bool:
    try:
        JoinRequest.objects.get(community=community, user=user)
        return True
    except JoinRequest.DoesNotExist:
        return False

def community_exists(community_slug:str)->bool:
    try :
            Community.objects.get(slug=community_slug)
            return True
    except Community.DoesNotExist:
        return False