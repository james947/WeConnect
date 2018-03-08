class User:
    count =0
    def __init__(self):
        self.users = []
        self.logged_in = {}
    
    def create_user(self, id, username, email, password):
        print('ddtuf',username,email,password)
        new_user = {
            'id':User.count +1,
            'username': username,
            'email': email,
            'password': password
        }

        self.users.append(new_user)
        User.count +=1
    
