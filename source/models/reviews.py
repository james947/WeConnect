class Reviews():
    count = 1
    def __init__(self,review):
        self.review = review
        self.id = Reviews.count
        Reviews.count+=1