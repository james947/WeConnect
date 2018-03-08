class Business():
    #initialize count to add when business is registered
    count =0
    def __init__(self):
        self.business=[]

    def create_business(self,id,businessname,description,location,category):

        new_business={
            'id':Business.count + 1,
            'businessname':businessname,
            'description':description,
            'location':location,
            'category':category,
                }

        self.business.append(new_business)
        Business.count +=1

        return self.business