with open('users.json') as file:
    print(len(json.load(file)['users']))
