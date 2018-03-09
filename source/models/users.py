class User:
    count =0
    def __init__(self):
        self.users = []
    
    def create_user(self, id, username, email, password):
        # print('ddtuf',username,email,password)
        id = len(self.users) +1
        new_user = {
            'id': id,
            'username': username,
            'email': email,
            'password': password
        }
        self.users.append(new_user)
    
    
