from django.test import TestCase
from django.utils import timezone
import datetime
from .models import Question
from django.urls import reverse

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

def create_question(question_text,days):

    """
    method creates question published in either the past or future
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text,pub_date=time)
    
class QuestionIndexViewTests(TestCase):

        """
        class facilitates the creation of test units to test index view class behavior
        """
        def test_no_questions(self):

            """
            method tests if an appropriate message is displayed if there are no questions
            """
            response = self.client.get(reverse('polls:index'))
            self.assertEqual(response.status_code,200)
            self.assertContains(response,"No polls are available")
            self.assertQuerysetEqual(response.context['latest_question_list'],[])
        
        def test_past_question(self):

            """
            method checks if questions with past pub_dates are displayed on the landing page
            """
            create_question(question_text="past question",days=-30)
            response = self.client.get(reverse('polls:index'))
            self.assertQuerysetEqual(
                response.context['latest_question_list'],['<Question: past question>']
            )
        
        def test_future_question(self):

            """
            method checks if questions with future pub_dates are not displayed on the landing page
            """
            create_question(question_text="future question",days=30)
            response = self.client.get(reverse('polls:index'))
            self.assertContains(response,"No polls are available")
            self.assertQuerysetEqual(response.context['latest_question_list'],[])
        
        def test_past_and_future_questions(self):

            """
            method checks if when both future and past questions are present only the past question is displayed
            """
            create_question(question_text="past question",days=-30)
            create_question(question_text="future question",days=30)
            response = self.client.get(reverse('polls:index'))
            self.assertQuerysetEqual(
                response.context['latest_question_list'],['<Question: past question>']
            )
        
        def test_two_past_questions(self):

            """
            method tests if multiple past questions are displayed on the landing page
            """
            create_question(question_text="past question 1",days=-30)
            create_question(question_text="past question 2",days=-60)
            response = self.client.get(reverse('polls:index'))
            self.assertQuerysetEqual(
                response.context['latest_question_list'],['<Question: past question 1>','<Question: past question 2>']
            )
