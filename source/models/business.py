class Business():
    count = 0
     #initialize count to add when business is registered
    def __init__(self,name,description,location,category):
        self.businessname = name
        self.description = description
        self.location = location
        self.category = category
        self.id = Business.count
        Business.count +=1