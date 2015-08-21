from django.shortcuts import render
from .models import SuccessVideo, SuccessStoryPerson, Snippet

from education.models import WorkingAt
from base_app.models import Partner


def index(request):
    successors = SuccessStoryPerson.objects.order_by('?')[:6]
    partners = Partner.objects.all().order_by('?')
    videos = SuccessVideo.objects.all()[:4]

    success_counter = WorkingAt.objects.filter(came_working=False).count()

    snippets = {snippet.label: snippet for snippet in Snippet.objects.all()}

    return render(request, "website/index.html", locals())


def about(request):
    snippets = {snippet.label: snippet for snippet in Snippet.objects.all()}
    return render(request, "website/about.html", locals())


def courses(request):
    snippets = {snippet.label: snippet for snippet in Snippet.objects.all()}
    return render(request, "website/courses.html", locals())


def partners(request):
    partners = Partner.objects.all().order_by('?')
    snippets = {snippet.label: snippet for snippet in Snippet.objects.all()}

    return render(request, "website/partners.html", locals())
