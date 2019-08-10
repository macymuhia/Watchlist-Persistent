class Movie:
    def __init__(self, id, title, overview, poster, rating, vote_count):
        self.id = id
        self.title = title
        self.overview = overview
        self.poster = "https://image.tmdb.org/t/p/w500/" + poster
        self.rating = rating
        self.vote_count = vote_count
