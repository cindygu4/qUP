from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import JoinClassForm
from apps.teachers.models import Classroom, Queue
from .models import Notification, Feedback
from apps.teachers.views import update_queue
from apps.users.models import Teacher, Student
from django.contrib import messages
from django.http import JsonResponse
import time

# Create your views here.
def is_student(user):
    return user.is_student

@login_required
@user_passes_test(is_student)
def index(request):
    return render(request, "students/index.html")

@login_required
@user_passes_test(is_student)
def join_class(request):
    if request.method == 'POST':
        form = JoinClassForm(request.POST)
        if form.is_valid():
            class_code = form.cleaned_data['class_code']
            if Classroom.objects.filter(code=class_code).exists():
                classroom = Classroom.objects.get(code=class_code)
                student = Student.objects.get(user=request.user)
                student.classrooms.add(classroom)
                return redirect('students:view_classes')
            else:
                messages.error(request, "No classrooms match this code. Try again.")
    else:
        form = JoinClassForm()

    return render(request, "students/join_class.html", {
        'form': form
    })

@login_required
@user_passes_test(is_student)
def view_classes(request):
    classrooms = Classroom.objects.filter(students__user=request.user)
    return render(request, "students/classes.html", {
        'classrooms': classrooms
    })

@login_required
@user_passes_test(is_student)
def upcoming_oh(request):
    # update all the queues in the classrooms that the student is in first
    all_queues = Queue.objects.filter(classroom__students__user=request.user, display=True)
    for queue in all_queues:
        update_queue(queue)

    # order the teacher's queues by date then start time
    queues = Queue.objects.filter(classroom__students__user=request.user, display=True, opened=False)\
        .order_by('date', 'start_time').exclude(done=True)
    return render(request, "students/upcoming_oh.html", {
        'queues': queues
    })

@login_required
@user_passes_test(is_student)
def view_notifications(request):
    return render(request, "students/notifications.html")


''' API for getting a student's notifications '''
@login_required
@user_passes_test(is_student)
def notifications(request):
    # get all the notifications that relates to the student, order by reverse date and time
    notification_list = Notification.objects.filter(queue__classroom__students__user=request.user)\
        .order_by('-date', '-time')

    # Get start and end points
    start = int(request.GET.get("start") or 0)
    end = int(request.GET.get("end") or (start + 9))

    if end > len(notification_list):
        end = len(notification_list)

    if start != 0:
        start -= 1

    # Generate list of notifications
    data = []
    for i in range(start, end):
        data.append(notification_list[i].serialize())

    # Artificially delay speed of response
    time.sleep(0.5)

    return JsonResponse({"notifications": data})
