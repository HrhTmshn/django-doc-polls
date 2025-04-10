from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.db.models import F
from django.utils import timezone
from django.views.decorators.http import require_POST


from .models import Choice, Question

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """ Return the last five published questions (not including those set to be published in the future). """
        return Question.objects.filter(pub_date__lte=timezone.now(), choice__isnull=False).distinct().order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """ Excludes any questions that aren't published yet. """
        return Question.objects.filter(pub_date__lte=timezone.now(), choice__isnull=False).distinct()

    def dispatch(self, request, *args, **kwargs):
        """Redirects to results if user already voted."""
        question_id = kwargs.get("pk")
        votes_record = request.session.get("votes_record", {})

        if str(question_id) in votes_record:
            return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))

        return super().dispatch(request, *args, **kwargs)

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

    def get_queryset(self):
        """ Excludes any questions that aren't published yet. """
        return Question.objects.filter(pub_date__lte=timezone.now(), choice__isnull=False).distinct()

    def get_context_data(self, **kwargs):
        """Adds total votes and vote percentage to context."""
        context = super().get_context_data(**kwargs)
        question = self.object
        choices = question.choice_set.all()
        total_votes = sum(choice.votes for choice in choices)

        for choice in choices:
            if total_votes > 0:
                choice.percentage = round((choice.votes / total_votes) * 100)
            else:
                choice.percentage = 0

        context["total_votes"] = total_votes
        context["choices_with_percent"] = choices
        return context

@require_POST
def vote(request, question_id):
    """Handles vote submission and saves it in session."""
    question = get_object_or_404(Question, pk=question_id)

    votes_record = request.session.get("votes_record", {})
    if str(question_id) in votes_record:
        return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))

    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()

        votes_record[str(question_id)] = str(selected_choice.id)
        request.session["votes_record"] = votes_record

        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

@require_POST
def change_vote(request, question_id):
    """Reverts the vote and redirects back to question detail."""
    votes_record = request.session.get("votes_record", {})
    question_id_str = str(question_id)

    if question_id_str in votes_record:
        choice_id = votes_record[question_id_str]
        try:
            choice = Choice.objects.get(pk=choice_id, question__id=question_id)
            if choice.votes > 0:
                choice.votes = F("votes") - 1
                choice.save()
        except Choice.DoesNotExist:
            pass
        del votes_record[question_id_str]
        request.session["votes_record"] = votes_record

    return HttpResponseRedirect(reverse("polls:detail", args=(question_id,)))