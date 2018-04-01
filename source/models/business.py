class Business():
    count = 0
     #initialize count to add when business is registered
    def __init__(self,businessname,description,location,category):
        self.businessname = businessname
        self.description = description
        self.location = location
        self.category = category
        self.id = Business.count
        Business.count +=1