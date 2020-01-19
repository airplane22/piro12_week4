from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.views import generic

from polls.models import Choice, Question

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


 
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     # output = ', '.join([q.question_text for q in 
#     # latest_qeustion_list])
#     # return HttpResponse(output)

#     # template = loader.get_template('polls/index.html')
#     # context = {
#         # 'latest_question_list': latest_qeustion_list,
#     # }
#     # return HttpResponse(template.render(context, request))
    

#     # 단축 기능
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'polls/index.html', context)



# def detail(request,question_id):
#     # return HttpResponse(f"You're looking at question {question_id}")

#     #404 에러 일으키기
#     try : 
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")
#     return render(request, 'polls/detail.html', {'question':
#     question})

#     #404에러 지름길 : get_object_or_404
#     # question = get_object_or_404(Question, pk=question_id)
#     # return render(request, 'polls/detail.html', {'question':
#     # question})

#     #get_list_or_404 : get() 대신 filter()

# def results(request, question_id):
#     # response = f"You're looking at the results of question {question_id}"
#     # return HttpResponse(response)

#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question'
#     :question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try :
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question':question,
            'error_message':"You didn't select a choice.",
        })
    else :
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))
