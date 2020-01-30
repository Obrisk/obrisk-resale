from django.db.utils import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView, ListView, DetailView
from django.views.decorators.csrf import csrf_exempt

from obrisk.utils.helpers import ajax_required
from obrisk.qa.models import Question, Answer
from obrisk.qa.forms import QuestionForm

class QuestionsIndexListView(ListView):
    """CBV to render a list view with all the registered questions."""
    model = Question
    paginate_by = 20
    context_object_name = "questions"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        #This query is too slow
        #context["popular_tags"] = Question.objects.get_counted_tags()
        context["active"] = "all"
        context["base_active"] = "q_and_a"
        return context


class QuestionAnsListView(QuestionsIndexListView):
    """CBV to render a list view with all question which have been already
    marked as answered."""
    def get_queryset(self, **kwargs):
        return Question.objects.get_answered()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["active"] = "answered"
        context["base_active"] = "q_and_a"

        return context


class QuestionListView(QuestionsIndexListView):
    """CBV to render a list view with all question which haven't been marked
    as answered."""
    def get_queryset(self, **kwargs):
        return Question.objects.get_unanswered()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["active"] = "unanswered"
        context["base_active"] = "q_and_a"
        return context


class QuestionDetailView(DetailView):
    """View to call a given Question object and to render all the details about
    that Question."""
    model = Question
    context_object_name = "question"


class CreateQuestionView(LoginRequiredMixin, CreateView):
    """
    View to handle the creation of a new question
    """
    form_class = QuestionForm
    template_name = "qa/question_form.html"
    message = _("Your question has been created.")

    def __init__(self, **kwargs):
        self.object = None
        super().__init__(**kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        form = QuestionForm(self.request.POST)
    
        if form.is_valid():
            return self.form_valid(form) 
        else:
            #ret = dict(errors=form.errors)
            print(form.errors)
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse("qa:index_noans")


class CreateAnswerView(LoginRequiredMixin, CreateView):
    """
    View to create new answers for a given question
    """
    model = Answer
    fields = ["content", ]
    message = _("Thank you! Your answer has been posted.")

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.question_id = self.kwargs["question_id"]
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse(
            "qa:question_detail", kwargs={"pk": self.kwargs["question_id"]})


@login_required
@ajax_required
@csrf_exempt
@require_http_methods(["GET"])
#The only reason this method is GET is because the server will return 403 on the live site,
#even when ignoring the csrf with exempt decorator. Need to fix this method to become post.
def question_vote(request):
    """Function view to receive AJAX call, returns the count of votes a given
    question has recieved."""
    question_id = request.GET["question"]
    value = None

    if request.GET["value"] == "U":
        value = True
    else:
        value = False

    question = Question.objects.get(pk=question_id)
    try:
        question.votes.update_or_create(
            user=request.user, defaults={"value": value}, )
        question.count_votes()
        return JsonResponse({"votes": question.total_votes})

    except IntegrityError:  # pragma: no cover
        return JsonResponse({'status': 'false',
                             'message': _("Database integrity error.")},
                            status=500)


@login_required
@ajax_required
@csrf_exempt
@require_http_methods(["GET"])
#The only reason this method is GET is because the server will return 403 on the live site,
#even when ignoring the csrf with exempt decorator. Need to fix this method to become post.
def answer_vote(request):
    """Function view to receive AJAX call, returns the count of votes a given
    answer has recieved."""
    answer_id = request.GET["answer"]
    value = None
    if request.GET["value"] == "U":
        value = True

    else:
        value = False

    answer = Answer.objects.get(uuid_id=answer_id)
    try:
        answer.votes.update_or_create(
            user=request.user, defaults={"value": value}, )
        answer.count_votes()
        return JsonResponse({"votes": answer.total_votes})

    except IntegrityError:  # pragma: no cover
        return JsonResponse({'status': 'false',
                             'message': _("Database integrity error.")},
                            status=500)


@login_required
@ajax_required
@csrf_exempt
@require_http_methods(["GET"])
#The only reason this method is GET is because the server will return 403 on the live site,
#even when ignoring the csrf with exempt decorator. Need to fix this method to become post.
def accept_answer(request):
    """Function view to receive AJAX call, marks as accepted a given answer for
    an also provided question."""
    answer_id = request.GET["answer"]
    answer = Answer.objects.get(uuid_id=answer_id)
    answer.accept_answer()
    return JsonResponse({'status': 'true'}, status=200)
