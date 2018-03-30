class Business():
    count = 1
     #initialize count to add when business is registered
    def __init__(self,name,description,location,category):
        self.name = name
        self.description = description
        self.location = location
        self.category = category
        self.id = Business.count
        Business.count +=1