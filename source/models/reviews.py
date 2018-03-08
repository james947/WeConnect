class Reviews():
    """initialize an empty dict to store reviews"""
    def __init__(self):
        self.reviews = []

    def create_user(self, id, username,title,reviews):
        """Create user then append to list reviews"""
        new_reviews = {
            'id':id,
            'username': username,
            'title':title,
            'review':reviews

        }

        self.reviews.append(new_reviews)
       