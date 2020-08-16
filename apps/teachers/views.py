from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Classroom, Queue
from apps.users.models import Teacher
from django.http import Http404
from .forms import NewClassroomForm, NewQueueForm
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.http import JsonResponse
import json
from datetime import datetime

# Create your views here.
def is_teacher(user):
    return user.is_teacher

@login_required
@user_passes_test(is_teacher)
def index(request):
    return render(request, "teachers/index.html")

@login_required
@user_passes_test(is_teacher)
def view_classes(request):
    teacher = request.user.teacher_profile
    classes = Classroom.objects.filter(teacher=teacher)
    return render(request, "teachers/classes.html", {
        'classes': classes
    })

@login_required
@user_passes_test(is_teacher)
def add_class(request):
    if request.method == 'POST':
        form = NewClassroomForm(request.POST)
        if form.is_valid():
            class_name = form.cleaned_data['name']
            class_code = get_random_string(length=7)
            Classroom.objects.create(name=class_name, teacher=request.user.teacher_profile, code=class_code)
            return redirect('teachers:view_classes')
    else:
        form = NewClassroomForm()
    return render(request, "teachers/add_class.html", {
        'form': form
    })

def view_class(request, class_id):
    classroom = Classroom.objects.get(pk=class_id)
    queues = Queue.objects.filter(classroom=classroom).order_by('date', 'start_time')
    empty = True
    if queues:
        empty = False

    open_list = []
    for queue in queues:
        if (queue.date == datetime.today().date()) and (queue.start_time <= datetime.today().time()):
            open_list.append(True)
        else:
            open_list.append(False)

    joined_list = zip(queues, open_list)

    return render(request, "teachers/classroom.html", {
        'classroom': classroom, 'queues': joined_list, 'empty_list': empty
    })

def upcoming_oh(request):
    # order the teacher's queues by date then start time
    queues = Queue.objects.filter(classroom__teacher=request.user.teacher_profile).order_by('date', 'start_time')
    return render(request, "teachers/upcoming_ohs.html", {
        'queues': queues
    })

def add_queue(request, class_id):
    classroom = Classroom.objects.get(pk=class_id)
    if request.method == 'POST':
        form = NewQueueForm(request.POST)
        if form.is_valid():
            queue_name = form.cleaned_data['name']
            date = form.cleaned_data['date']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            location = form.cleaned_data['location']
            description = form.cleaned_data['description']

            # if end time is before start time, show a message
            if end_time <= start_time:
                messages.error(request, 'End Time should be later than Start Time.')
                return render(request, "teachers/add_queue.html", {
                    'classroom': classroom, 'form': form
                })
            else:
                Queue.objects.create(name=queue_name, classroom=classroom, date=date, start_time=start_time,
                                     end_time=end_time, location=location, description=description)
                return redirect('teachers:view_class', classroom.id)
    else:
        form = NewQueueForm()
    return render(request, "teachers/add_queue.html", {
        'classroom': classroom, 'form': form
    })

def open_queue(request, queue_id):
    queue = Queue.objects.filter(pk=queue_id).update(opened=True)
    return redirect('teachers:opened_queue', queue_id)

def opened_queue(request, queue_id):
    queue = Queue.objects.get(pk=queue_id)
    return render(request, "teachers/opened_oh.html", {
        'queue': queue
    })

@login_required
def edit_class_name(request, class_id):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    new_name = data.get("new_name", "")

    Classroom.objects.filter(pk=class_id).update(name=new_name)
    return JsonResponse({"message": "Class name edited successfully."}, status=201)

@login_required
def edit_queue(request, queue_id):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)

    return JsonResponse({"message": "Queue edited successfully."}, status=201)

@login_required
def delete_queue(request, queue_id):
    if Queue.objects.filter(pk=queue_id).exists():
        Queue.objects.filter(pk=queue_id).delete()
    else:
        raise Http404("Queue does not exist")

    return JsonResponse({"message": "Queue deleted successfully."}, status=201)
