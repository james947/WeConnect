class Reviews():
    """increments review by one"""
    count = 0
    def __init__(self,title,description,business_id):
        self.title=title
        self.description = description
        self.business_id = business_id
        self.id = Reviews.count
        Reviews.count+=1