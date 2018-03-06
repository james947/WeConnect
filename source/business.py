class Business():
    #initialize count to add when business is registered
    count = 1
    def __init__(self,name,description,location,category):
        self.name = name
        self.description = description
        self.location = location
        self.category = category
        self.id = Business.count
        Business.count +=1