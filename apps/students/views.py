from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import JoinClassForm
from apps.teachers.models import Classroom, Queue
from .models import Notification, Feedback, OfficeHoursLine
from apps.teachers.views import update_queue
from apps.users.models import Teacher, Student
from django.contrib import messages
from django.http import JsonResponse, Http404
from django.utils import timezone
import time

# Create your views here.
def is_student(user):
    return user.is_student

@login_required
@user_passes_test(is_student)
def index(request):
    # update all the queues in the classrooms that the student is in first
    all_queues = Queue.objects.filter(classroom__students__user=request.user, display=True)
    for single_queue in all_queues:
        update_queue(single_queue)

    current_queues = Queue.objects.filter(classroom__students__user=request.user, currently_meeting=True,
                                          done=False, display=True)
    finished_queues = Queue.objects.filter(classroom__students__user=request.user, done=True, display=True)

    # get the recently finished queues (finished within the last 7 days
    recently_finished = []
    for item in finished_queues:
        delta = timezone.localtime(timezone.now()).date() - item.date
        if delta.days <= 7:
            recently_finished.append(item)

    # get the queues that the student attended and finished within the past 7 days
    recently_attended = []
    feedback = []
    student = request.user.student_profile
    for queue in recently_finished:
        if OfficeHoursLine.objects.filter(queue=queue, student=student).exists():
            oh_help_list = OfficeHoursLine.objects.filter(queue=queue, student=student)
            student_got_help = False
            for new_help in oh_help_list:
                if new_help.got_help:
                    student_got_help = True

            # if the student got help, then create a feedback if not created yet
            if student_got_help:
                recently_attended.append(queue)
                new_feedback = Feedback.objects.get_or_create(student=student, queue=queue)
                feedback.append(new_feedback)

    recently_attended = zip(recently_attended, feedback)

    return render(request, "students/index.html", {
        'current_queues': current_queues, 'recently_attended': recently_attended
    })

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
    # update all the queues in the classrooms that the student is in first
    all_queues = Queue.objects.filter(classroom__students__user=request.user, display=True)
    for queue in all_queues:
        update_queue(queue)

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

@login_required
@user_passes_test(is_student)
def opened_queue(request, queue_id):
    queue = Queue.objects.get(pk=queue_id)
    oh_line = OfficeHoursLine.objects.filter(queue=queue, got_help=False).order_by('time_joined')
    already_joined = False
    if OfficeHoursLine.objects.filter(queue=queue, student=request.user.student_profile, got_help=False).exists():
        already_joined = True

    return render(request, "students/opened_queue.html", {
        'queue': queue, 'oh_line': oh_line, 'already_joined': already_joined
    })

@login_required
@user_passes_test(is_student)
def join_queue(request, queue_id):
    if Classroom.objects.filter(students__user=request.user).exists() and Queue.objects.filter(pk=queue_id).exists():
        # allow them to join the queue
        queue = Queue.objects.get(pk=queue_id)
        if not OfficeHoursLine.objects.filter(queue=queue, student=request.user.student_profile, got_help=False).exists():
            OfficeHoursLine.objects.create(queue=queue, student=request.user.student_profile,
                                           time_joined=timezone.localtime(timezone.now()).time())
    else:
        raise Http404

    return redirect('students:opened_queue', queue_id)

@login_required
@user_passes_test(is_student)
def give_feedback(request, queue_id):
    queue = Queue.objects.get(pk=queue_id)
    student = request.user.student_profile
    feedback = Feedback.objects.get_or_create(student=student, queue=queue)
    return render(request, "students/give_feedback.html", {
        'queue': queue, 'feedback': feedback
    })
