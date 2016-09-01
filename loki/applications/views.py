from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404

from loki.website.models import CourseDescription, Snippet
from loki.education.models import Course

from .forms import ApplyForm
from .models import (Application, ApplicationInfo,
                     ApplicationProblem, ApplicationProblemSolution)


@login_required(login_url='website:login')
def apply_course(request, course_url):
    cd = get_object_or_404(CourseDescription, url=course_url)

    try:
        course = cd.course
        if course:
            app_info = ApplicationInfo.objects.get(course=course)
            if not app_info.apply_is_active():
                return redirect(reverse('website:apply_overview'))
            app_problems = ApplicationProblem.objects.filter(application_info=app_info)
    except (ApplicationInfo.DoesNotExist, ApplicationProblem.DoesNotExist) as err:
        return redirect(reverse('website:profile'))

    if Application.objects.filter(user=request.user, application_info=app_info).exists():
        return redirect(reverse('website:edit_applications'))

    apply_form = ApplyForm(tasks=app_problems.count(), app_problems=app_problems)
    problems = list(range(len(apply_form.fields) - len(app_problems))) + list(app_problems)

    if request.method == 'POST':
        apply_form = ApplyForm(request.POST, tasks=app_problems.count(),
                                             app_problems=app_problems)

        if apply_form.is_valid():
            apply_form.save(app_info, app_problems, request.user)
            return render(request, 'already_applied.html', locals())

    return render(request, 'apply.html', locals())

def apply_overview(request):
    courses = [x for x in Course.objects.all() \
                    if getattr(x, 'applicationinfo', None) is not None and \
                       getattr(x, 'coursedescription', None) is not None]
    apply_courses = [x for x in courses if x.applicationinfo.apply_is_active()]
    if not apply_courses:
        raise Http404("Page not found")

    snippets = {snippet.label: snippet for snippet in Snippet.objects.all()}

    return render(request, 'apply_overview.html', locals())

@login_required(login_url='website:login')
def edit_applications(request):
    user_applications = Application.objects.filter(user=request.user).all()
    app_form = {}

    for application in user_applications:
        tasks = application.application_info.applicationproblem_set.all()
        initial_data = {'phone': application.phone,
                        'skype': application.skype,
                        'works_at': application.works_at,
                        'studies_at': application.studies_at}
        for index, task in enumerate(tasks):
            solution = task.applicationproblemsolution.solution_url
            initial_data['task_{0}'.format(index+1)] = solution

        form = ApplyForm(tasks=tasks.count(), app_problems=tasks,
                         initial=initial_data)

        app_form[application.application_info.course] = form
        if request.method == 'POST':
            form = ApplyForm(request.POST, tasks=tasks.count(), app_problems=tasks,
                             initial=initial_data)
            if form.is_valid():
                form.update(application.application_info, tasks, request.user)
                app_form[application.application_info.course] = form

    return render(request, 'edit_applications.html', locals())
