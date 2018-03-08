class Business():
    #initialize count to add when business is registered
 
    def __init__(self):
        self.business=[]

    def create_business(self,id,businessname,description,location,category):
        count =0
        new_business={
            'id':count + 1,
            'businessname':businessname,
            'description':description,
            'location':location,
            'category':category,
                }

        self.business.append(new_business)

        return self.business