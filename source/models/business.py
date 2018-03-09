class Business():
    #initialize count to add when business is registered
    count =1
    def __init__(self):
        self.business=[]

    def create_business(self,id,businessname,description,location,category):
        id = len(self.business) +1
        new_business={
            'id':id,
            'businessname':businessname,
            'description':description,
            'location':location,
            'category':category,
                }

        self.business.append(new_business)
