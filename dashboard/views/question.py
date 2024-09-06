from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from ..models import CommonQuestion
from ..forms.question import CommonQuestionForm

def common_question_list(request):
    common_questions = CommonQuestion.objects.all()
    paginator = Paginator(common_questions,5 )  # Show 10 common questions per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number
                                  )
    return render(request, 'question/list.html', {'page_obj': page_obj})

def common_question_create(request):
    if request.method == 'POST':
        form = CommonQuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('common_question_list')
    else:
        form = CommonQuestionForm()
    return render(request, 'question/create.html', {'form': form})

def common_question_update(request, pk):
    common_question = get_object_or_404(CommonQuestion, pk=pk)
    if request.method == 'POST':
        form = CommonQuestionForm(request.POST, instance=common_question)
        if form.is_valid():
            form.save()
            return redirect('common_question_list')
    else:
        form = CommonQuestionForm(instance=common_question)
    return render(request, 'question/update.html', {'form': form,'common_question':common_question})

def common_question_delete(request, pk):
    common_question = get_object_or_404(CommonQuestion, pk=pk)
    if request.method == 'POST':
        common_question.delete()
        return redirect('common_question_list')
