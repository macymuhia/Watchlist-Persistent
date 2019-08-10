import unittest
from app.models import Review


class ReviewTest(unittest.TestCase):
    '''
    Test Class to test the behaviour of the Review class
    '''
    def setUp(self):

        self.new_review = Review(1234, "Oceans8", "https://image.tmdb.org/t/p/w500/khsjha27hbs", "khsjha27hbs")

    def test_instance(self):
        self.assertTrue(isinstance(self.new_review, Review))

    def test_init(self):
        self.assertEqual(self.new_review.movie_id, 1234)

        self.assertEqual(self.new_review.title, "Oceans8")

        self.assertEqual(
            self.new_review.image_url, "https://image.tmdb.org/t/p/w500/khsjha27hbs"
        )

        self.assertEqual(self.new_review.review, "khsjha27hbs")
