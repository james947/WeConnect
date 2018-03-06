class User:
    count =1 #icrease user id when he/she signs up
    """"""
    def __init__(self,username,email,password):
        self.username = username
        self.email =email
        self.password = password
        self.id = User.count
        User.count +=1
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)