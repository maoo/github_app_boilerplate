import easycla_api
import gh_api

finos_members = gh_api.get_members_and_invites("finos")
print (f"FINOS Members (and invites): {len(finos_members)}")
easycla_users = easycla_api.get_easycla_gh_usernames()
print (f"EasyCLA GH users: {len(easycla_users)}")

to_invite = []
for user in easycla_users:
    if not user in finos_members:
        # print(f"User {user} should be invited")
        to_invite.append(user)

remove_member = []
for user in finos_members:
    if not user in easycla_users:
        # print(f"User {user} should not be a FINOS member")
        remove_member.append(user)

print (f"To Invite: {len(to_invite)}")
print (f"To Remove as Member: {len(remove_member)}")
