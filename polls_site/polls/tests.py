import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question, Choice

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """ was_published_recently() returns False for questions whose pub_date is in the future. """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """ was_published_recently() returns False for questions whose pub_date is older than 1 day. """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)


    def test_was_published_recently_with_recent_question(self):
        """was_published_recently() returns True for questions whose pub_date is within the last day. """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

def create_question(question_text, days, choices=tuple("Default Choice")):
    """ Create a question with the given `question_text` and published the given number of `days` offset to now (negative for questions published in the past, positive for questions that have yet to be published). """
    time = timezone.now() + datetime.timedelta(days=days)
    question = Question.objects.create(question_text=question_text, pub_date=time)
    if choices:
        Choice.objects.bulk_create([Choice(question=question, choice_text=choice) for choice in choices])
    return question 

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """ If no questions exist, an appropriate message is displayed. """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """ Questions with a pub_date in the past are displayed on the index page. """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_future_question(self):
        """ Questions with a pub_date in the future aren't displayed on the index page. """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        """ Even if both past and future questions exist, only past questions are displayed. """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_two_past_questions(self):
        """ The questions index page may display multiple questions. """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question2, question1],
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """ The detail view of a question with a pub_date in the future returns a 404 not found. """
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """ The detail view of a question with a pub_date in the past displays the question's text. """
        past_question = create_question(question_text="Past Question", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class QuestionResultsViewTests(TestCase):
    def test_future_question(self):
        """ The result view of a question with a pub_date in the future returns a 404 not found. """
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("polls:results", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """ The result view of a question with a pub_date in the past displays the question's text. """
        past_question = create_question(question_text="Past Question", days=-5)
        url = reverse("polls:results", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class ChoicesIndexViewTests(TestCase):
    def test_question_no_choices(self):
        """ Questions without a choices aren't displayed on the index page. """
        create_question(question_text="Question without choices.", days=0, choices=None)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])
    
    def test_question_with_choices(self):
        """ Questions with a choices are displayed on the index page. """
        question = create_question(question_text="Question with choices.", days=0, choices=["First choice.", "Second choice."])
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"], [question])


class ChoicesDetailViewTests(TestCase):
    def test_question_no_choices(self):
        """ Questions without a choices aren't displayed on the detail page. """
        question = create_question(question_text="Question without choices.", days=0, choices=None)
        url = reverse("polls:detail", args=(question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_question_with_choices(self):
        """ Questions with a choices are displayed on the detail page. """
        question = create_question(question_text="Question with choices.", days=0, choices=["First choice.", "Second choice."])
        url = reverse("polls:detail", args=(question.id,))
        response = self.client.get(url)
        self.assertContains(response, question.question_text)


class ChoicesResultsViewTests(TestCase):
    def test_question_no_choices(self):
        """ Questions without a choices aren't displayed on the result page. """
        question = create_question(question_text="Question without choices.", days=0, choices=None)
        url = reverse("polls:results", args=(question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_question_with_choices(self):
        """ Questions with a choices are displayed on the result page. """
        question = create_question(question_text="Question with choices.", days=0, choices=["First choice.", "Second choice."])
        url = reverse("polls:results", args=(question.id,))
        response = self.client.get(url)
        self.assertContains(response, question.question_text)