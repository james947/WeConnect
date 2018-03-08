class User:
    count =1 #icrease user id when user signs up
    
    def __init__(self,username,email,password):
        self.username = username
        self.email =email
        self.password = password
        self.id = User.count
        User.count +=1