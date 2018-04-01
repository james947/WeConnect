class Reviews():
    """increments review by one"""
    count = 0
    def __init__(self,title,description,business_id):
        self.description = description
        self.id = Reviews.count
        Reviews.count+=1