from django.shortcuts import render, redirect

from .models import Topic
from .forms import TopicForm, EntryForm


# Create your views here.


def index(request):
    """Home page for User Account"""
    return render(request, 'User_Accounts/index.html')


def topics(request):
    topics = Topic.objects.order_by('-date_added')
    context = {'topics': topics}
    return render(request, 'User_Accounts/topics.html', context)


def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'User_Accounts/topic.html', context)


def new_topic(request):
    if request.method != 'POST':  # 1
        form = TopicForm()  # 2
    else:
        form = TopicForm(data=request.POST)  # 3
        if form.is_valid():  # 4
            form.save()  # 5
            return redirect('User_Accounts:topics')  # 6
    context = {'form': form}  # 7
    return render(request, 'User_Accounts/new_topic.html', context)


def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)  # 1
    if request.method != 'POST':  # 2
        form = EntryForm()  # 3
    else:
        form = EntryForm(data=request.POST)  # 4
        if form.is_valid():
            new_entry = form.save(commit=False)  # 5
            new_entry.topic = topic  # 6
            new_entry.save()
            return redirect('User_Accounts:topic', topic_id=topic_id)  # 7
    context = {'topic': topic, 'form': form}
    return render(request, 'User_Accounts/new_entry.html', context)
