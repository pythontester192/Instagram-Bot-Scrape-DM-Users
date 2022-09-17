import json
import random
from src.instadm import InstaDM

f = open('infos/accounts.json',)
accounts = json.load(f)

with open('infos/usernames.txt', 'r') as f:
    usernames = [line.strip() for line in f]

with open('infos/messages.txt', 'r') as f:
    messages = [line.strip() for line in f]

while True:
    if not usernames:
        print('Finished usernames.')
        break
    
    dm_num = int(input('How many DM you want to send in each account: '))

    for account in accounts:
        if not usernames:
            break
        # Auto login
        insta = InstaDM(username=account["username"],
                        password=account["password"], headless=False)

        for i in range(dm_num):

            if not usernames:
                break

            username = usernames.pop()
            # Send message
            insta.sendMessage(
                user=username, message=random.choice(messages))

        insta.teardown()
