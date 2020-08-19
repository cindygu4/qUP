from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Classroom, Queue
from apps.users.models import Teacher
from apps.students.models import Notification, Feedback, OfficeHoursLine
from django.http import Http404
from .forms import NewClassroomForm, NewQueueForm
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
import json
from django.db.models import Avg
import pytz
from datetime import date

# Create your views here.
def is_teacher(user):
    return user.is_teacher

''' Helper function to update a queue '''
def update_queue(queue):
    # if the queue date and time are within the bounds then update currently meeting to true
    if (queue.date == timezone.localtime(timezone.now()).date()) and (queue.start_time <= timezone.localtime(
            timezone.now()).time()) and (queue.end_time >= timezone.localtime(timezone.now()).time()):

        if not queue.currently_meeting:
            Queue.objects.filter(pk=queue.id).update(currently_meeting=True)

    # else if the queue date is past or the end time has passed, then set done = True and currently_meeting = False
    elif (queue.date < timezone.localtime(timezone.now()).date()) or ((queue.date == timezone.localtime(
            timezone.now()).date()) and (queue.end_time <= timezone.localtime(timezone.now()).time())):

        if not queue.done or queue.currently_meeting:
            Queue.objects.filter(pk=queue.id).update(done=True)
            Queue.objects.filter(pk=queue.id).update(currently_meeting=False)
    else:
        if queue.currently_meeting:
            Queue.objects.filter(pk=queue.id).update(currently_meeting=False)
    return

@login_required
@user_passes_test(is_teacher)
def index(request):
    teacher = request.user.teacher_profile

    # first update all the queues
    all_queues = Queue.objects.filter(classroom__teacher=teacher, display=True)
    for single_queue in all_queues:
        update_queue(single_queue)

    current_queues = Queue.objects.filter(classroom__teacher=teacher, currently_meeting=True, done=False, display=True)\
        .order_by('start_time')
    finished_queues = Queue.objects.filter(classroom__teacher=teacher, done=True, display=True).order_by('-date',
                                                                                                         '-start_time')

    # get the recently finished queues (finished within the last 7 days
    recently_finished = []
    for queue in finished_queues:
        delta = timezone.localtime(timezone.now()).date() - queue.date
        if delta.days <= 7:
            recently_finished.append(queue)

    return render(request, "teachers/index.html", {
        'current_queues': current_queues, 'recently_finished': recently_finished
    })


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

@login_required
@user_passes_test(is_teacher)
def view_class(request, class_id):
    classroom = Classroom.objects.get(pk=class_id)
    queues = Queue.objects.filter(classroom=classroom, display=True)
    empty = True
    if queues:
        empty = False

    for queue in queues:
        update_queue(queue)

    updated_queues = Queue.objects.filter(classroom=classroom, display=True)\
        .order_by('done', '-currently_meeting', 'date', 'start_time')

    return render(request, "teachers/classroom.html", {
        'classroom': classroom, 'queues': updated_queues, 'empty_list': empty
    })

@login_required
@user_passes_test(is_teacher)
def upcoming_oh(request):
    # update the queues first
    teacher = request.user.teacher_profile
    all_queues = Queue.objects.filter(classroom__teacher=teacher, display=True)
    for queue in all_queues:
        update_queue(queue)

    # order the teacher's unopened and unfinished queues by date then start time
    queues = Queue.objects.filter(classroom__teacher=teacher, display=True, opened=False)\
        .order_by('date', 'start_time').exclude(done=True)
    return render(request, "teachers/upcoming_ohs.html", {
        'queues': queues
    })

@login_required
@user_passes_test(is_teacher)
def add_queue(request, class_id):
    classroom = Classroom.objects.get(pk=class_id)
    if request.method == 'POST':
        form = NewQueueForm(request.POST)
        if form.is_valid():
            queue_name = form.cleaned_data['name']
            queue_date = form.cleaned_data['date']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            location = form.cleaned_data['location']
            description = form.cleaned_data['description']
            meeting_url = form.cleaned_data['meeting_url']

            # if end time is before start time, show a message
            if end_time <= start_time:
                messages.error(request, 'End Time should be later than Start Time.')
                return render(request, "teachers/add_queue.html", {
                    'classroom': classroom, 'form': form
                })
            else:
                if meeting_url is None or meeting_url == '':
                    q = Queue.objects.create(name=queue_name, classroom=classroom, date=queue_date,
                                             start_time=start_time,
                                             end_time=end_time, location=location, description=description,
                                             meeting_url=meeting_url, has_meeting_url=False)
                else:
                    q = Queue.objects.create(name=queue_name, classroom=classroom, date=queue_date,
                                             start_time=start_time,
                                             end_time=end_time, location=location, description=description,
                                             meeting_url=meeting_url, has_meeting_url=True)

                Notification.objects.create(queue=q, content="Instructor has created this new office hours.",
                                            date=timezone.localtime(timezone.now()).date(),
                                            time=timezone.localtime(timezone.now()).time())

                return redirect('teachers:view_class', classroom.id)
    else:
        form = NewQueueForm()
    return render(request, "teachers/add_queue.html", {
        'classroom': classroom, 'form': form
    })

@login_required
@user_passes_test(is_teacher)
def open_queue(request, queue_id):
    queue = Queue.objects.filter(pk=queue_id)
    queue.update(opened=True)
    queue.update(currently_meeting=True)

    # Notify students of the queue being opened
    q = Queue.objects.get(pk=queue_id)
    Notification.objects.create(queue=q, content="Instructor has opened the queue for this office hours.",
                                date=timezone.localtime(timezone.now()).date(),
                                time=timezone.localtime(timezone.now()).time())

    all_queues = Queue.objects.filter(classroom__teacher=request.user.teacher_profile, display=True)
    for item in all_queues:
        update_queue(item)

    return redirect('teachers:opened_queue', queue_id)

@login_required
@user_passes_test(is_teacher)
def opened_queue(request, queue_id):
    queue = Queue.objects.get(pk=queue_id)
    oh_line = OfficeHoursLine.objects.filter(queue=queue, got_help=False).order_by('time_joined')
    return render(request, "teachers/opened_oh.html", {
        'queue': queue, 'oh_line': oh_line
    })

@login_required
@user_passes_test(is_teacher)
def edit_class_name(request, class_id):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    new_name = data.get("new_name", "")

    Classroom.objects.filter(pk=class_id).update(name=new_name)
    return JsonResponse({"message": "Class name edited successfully."}, status=201)

@login_required
@user_passes_test(is_teacher)
def edit_queue(request, queue_id):
    queue = Queue.objects.get(pk=queue_id)
    if request.method == 'POST':
        form = NewQueueForm(request.POST)
        if form.is_valid():
            queue_name = form.cleaned_data['name']
            queue_date = form.cleaned_data['date']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            location = form.cleaned_data['location']
            description = form.cleaned_data['description']
            meeting_url = form.cleaned_data['meeting_url']

            # if end time is before start time, show a message
            if end_time <= start_time:
                messages.error(request, 'End Time should be later than Start Time.')
                return render(request, "teachers/add_queue.html", {
                    'form': form
                })
            else:
                has_url = False
                if meeting_url is not None:
                    has_url = True
                Queue.objects.filter(pk=queue_id).update(name=queue_name, date=queue_date, start_time=start_time,
                                                         end_time=end_time, location=location, description=description,
                                                         meeting_url=meeting_url, has_meeting_url=has_url)

                q = Queue.objects.get(pk=queue_id)
                Notification.objects.create(queue=q, content="Instructor has made changes to this office hours.",
                                            date=timezone.localtime(timezone.now()).date(),
                                            time=timezone.localtime(timezone.now()).time())

                return redirect('teachers:view_class', queue.classroom.id)
    else:
        form = NewQueueForm(initial={'name': queue.name, 'location': queue.location, 'meeting_url': queue.meeting_url,
                                     'date': queue.date, 'start_time': queue.start_time, 'end_time': queue.end_time,
                                     'description': queue.description})

    return render(request, "teachers/edit_queue.html", {
        'queue': queue, 'form': form
    })

@login_required
@user_passes_test(is_teacher)
def delete_queue(request, queue_id):
    if Queue.objects.filter(pk=queue_id).exists():
        # don't actually delete queue, just update it
        Queue.objects.filter(pk=queue_id).update(display=False)
        q = Queue.objects.get(pk=queue_id)
        Notification.objects.create(queue=q, content="Instructor has deleted this office hours.",
                                    date=timezone.localtime(timezone.now()).date(),
                                    time=timezone.localtime(timezone.now()).time())
    else:
        raise Http404("Queue does not exist")

    queue = Queue.objects.get(pk=queue_id)

    return redirect('teachers:view_class', queue.classroom.id)

@login_required()
@user_passes_test(is_teacher)
def delete_class(request, class_id):
    if Classroom.objects.filter(pk=class_id).exists():
        Classroom.objects.filter(pk=class_id).delete()
    else:
        raise Http404

    return redirect('teachers:view_classes')

@login_required()
@user_passes_test(is_teacher)
def finished_helping(request, line_id):
    line_item = OfficeHoursLine.objects.get(pk=line_id)
    OfficeHoursLine.objects.filter(pk=line_id).update(got_help=True)
    return redirect('teachers:opened_queue', line_item.queue.id)

@login_required()
@user_passes_test(is_teacher)
def end_queue(request, queue_id):
    Queue.objects.filter(pk=queue_id).update(done=True, currently_meeting=False)
    q = Queue.objects.get(pk=queue_id)
    Notification.objects.create(queue=q, content="Instructor has ended this office hours.",
                                date=timezone.localtime(timezone.now()).date(),
                                time=timezone.localtime(timezone.now()).time())
    return redirect('teachers:index')

@login_required()
@user_passes_test(is_teacher)
def view_feedback(request, queue_id):
    queue = Queue.objects.get(pk=queue_id)
    feedback_list = Feedback.objects.filter(queue=queue, completed=True)
    num_completed = Feedback.objects.filter(queue=queue, completed=True).count()
    avg_rating = Feedback.objects.filter(queue=queue, completed=True).aggregate(avg_rating=Avg('rating'))
    return render(request, "teachers/feedback.html", {
        'queue': queue, 'feedback_list': feedback_list, 'num_completed': num_completed, 'avg_rating': avg_rating
    })
