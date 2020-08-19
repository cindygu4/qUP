from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import JoinClassForm, JoinQueueForm
from apps.teachers.models import Classroom, Queue
from .models import Notification, Feedback, OfficeHoursLine
from apps.teachers.views import update_queue
from apps.users.models import Teacher, Student
from django.contrib import messages
from django.http import JsonResponse, Http404
from django.utils import timezone
import time
import json

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
                                          done=False, display=True).order_by('start_time')
    finished_queues = Queue.objects.filter(classroom__students__user=request.user, done=True, display=True)\
        .order_by('-date', '-start_time')

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
                feedback.append(new_feedback[0])

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

    num_students = OfficeHoursLine.objects.filter(queue=queue, got_help=False).count()

    return render(request, "students/opened_queue.html", {
        'queue': queue, 'oh_line': oh_line, 'already_joined': already_joined, 'form': JoinQueueForm(),
        'num_students': num_students
    })

@login_required
@user_passes_test(is_student)
def join_queue(request, queue_id):
    if request.method == 'POST':
        form = JoinQueueForm(request.POST)
        if form.is_valid():
            location = form.cleaned_data['location']
            meeting_url = form.cleaned_data['meeting_url']
            description = form.cleaned_data['description']

            if Classroom.objects.filter(students__user=request.user).exists() and Queue.objects.filter(pk=queue_id).exists():
                # allow them to join the queue
                queue = Queue.objects.get(pk=queue_id)
                if not OfficeHoursLine.objects.filter(queue=queue, student=request.user.student_profile, got_help=False)\
                        .exists():
                    student = request.user.student_profile
                    if meeting_url is None or meeting_url == '':
                        OfficeHoursLine.objects.create(queue=queue, student=student, location=location,
                                                       time_joined=timezone.localtime(timezone.now()).time(),
                                                       has_student_url=False, student_url=meeting_url,
                                                       description=description)
                    else:
                        OfficeHoursLine.objects.create(queue=queue, student=student, location=location,
                                                       has_student_url=True, student_url=meeting_url,
                                                       time_joined=timezone.localtime(timezone.now()).time(),
                                                       description=description)
            else:
                raise Http404

    return redirect('students:opened_queue', queue_id)

@login_required
@user_passes_test(is_student)
def give_feedback(request, queue_id):
    queue = Queue.objects.get(pk=queue_id)
    student = request.user.student_profile
    feedback = Feedback.objects.get_or_create(student=student, queue=queue)

    # if student already completed feedback, redirect them to the dashboard
    if feedback[0].completed:
        return redirect('students:index')

    return render(request, "students/give_feedback.html", {
        'queue': queue, 'feedback': feedback[0]
    })

'''API for submitting a feedback form'''
@login_required
@user_passes_test(is_student)
def submit_feedback(request, feedback_id):
    # cannot get the feedback object, just post
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    try:
        feedback = Feedback.objects.get(pk=feedback_id)
    except Feedback.DoesNotExist:
        return JsonResponse({"error": "Feedback entry not found."}, status=404)

    try:
        data = json.loads(request.body)
    except ValueError:
        queue = Queue.objects.get(pk=feedback.queue.id)
        return redirect('students:give_feedback', queue.id)

    rating = data.get("rating", "")
    if rating == 0:
        queue = Queue.objects.get(pk=feedback.queue.id)
        return redirect('students:give_feedback', queue.id)

    comments = data.get("comments", "")

    Feedback.objects.filter(pk=feedback_id).update(rating=rating)
    Feedback.objects.filter(pk=feedback_id).update(comments=comments)
    Feedback.objects.filter(pk=feedback_id).update(completed=True)

    return JsonResponse({"message": "Feedback submitted successfully."}, status=201)
