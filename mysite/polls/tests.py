from django.test import TestCase
from django.utils import timezone
import datetime
from .models import Question

# Create your tests here.

class QuestionModelTests(TestCase):

    """
    class facilitates the creation of test units to test Question model behavior
    """

    def setUp(self):

        """
        method runs before all tests
        """
        self.question = Question("what is your name?",'2020-05-20')

    def test_init(self):

        """
        method checks if objects are initialized properly
        """
        self.assertTrue(isinstance(self.question,Question))

    def test_was_published_recently_with_future_question(self):

        """
        method tests if app's was_published_recently() returns false if a question with a future date is created
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(),False)

    def test_was_published_recently_with_old_question(self):

        """
        method tests if app's was_published_recently() returns false if a question whose pub_date is older than 1 day is created
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(),False)

    def test_was_published_recently_with_recent_question(self):

        """
        method tests if app's was_published_recently() returns true if a question whose pub_date is less than a day is published
        """
        time = timezone.now() - datetime.timedelta(minutes=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(),True)
