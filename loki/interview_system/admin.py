from django.contrib import admin

from .models import Interviewer, InterviewerFreeTime, Interview


@admin.register(Interviewer)
class InterviewerAdmin(admin.ModelAdmin):

    list_display = ['interviewer', ]

    def has_module_permission(self, request):
        return True


@admin.register(InterviewerFreeTime)
class InterviewerFreeTimeAdmin(admin.ModelAdmin):

    list_display = [
        'interviewer',
        'date',
        'start_time',
        'end_time',
    ]
    search_fields = ['interviewer__email', 'interviewer__first_name']
    list_filter = ['date', ]

    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):

    list_display = [
        'date',
        'start_time',
        'get_interviewer',
        'get_applying_student',
        'get_student_skype',
        'get_student_application_course',
        'has_received_email',
        'get_interview_confirmation',
        'get_tasks',
        'get_code_skills',
        'get_code_design',
        'get_fit_attitude',
        'is_accepted',
    ]
    search_fields = ['interviewer__email', 'interviewer__first_name', 'date']
    list_filter = ['date', 'start_time']

    def get_applying_student(self, obj):
        if not obj.application:
            return
        link_format = u"<a href='../../base_app/baseuser/{id}/'>{name}</a>"
        return link_format.format(id=obj.application.user.id,
                                  name=obj.application.user.full_name)

    get_applying_student.empty_value_display = 'Free slot'
    get_applying_student.short_description = "Student"
    get_applying_student.allow_tags = True

    def get_student_skype(self, obj):
        if not obj.application:
            return

        return obj.application.skype

    get_student_skype.empty_value_display = 'Free slot'
    get_student_skype.short_description = "Student skype"

    def get_interviewer(self, obj):
        return obj.interviewer.full_name

    get_interviewer.short_description = "Interviewer"

    def get_student_application_course(self, obj):
        if not obj.application:
            return

        return obj.application.application_info

    get_student_application_course.empty_value_display = 'Free slot'
    get_student_application_course.short_description = "Applying for"

    def get_interview_confirmation(self, obj):
        return obj.has_confirmed

    get_interview_confirmation.short_description = "Confirmed interview"
    get_interview_confirmation.boolean = True

    def get_tasks(self, obj):
        if not obj.application:
            return

        ordered_list_format = "<ol>{list_items}</ol>"
        list_element_format = u"<li><a href='{url}'>{name}</a></li>"

        result = []
        problems = obj.application.application_info.applicationproblem_set.all()

        for index in range(problems.count()):
            problem = problems[index]
            solution = obj.application.applicationproblemsolution_set\
                          .filter(problem=problem).first()

            if not solution:
                continue

            result.append(list_element_format.format(url=solution.solution_url,
                                                     name=problem.name))

        return ordered_list_format.format(list_items=''.join(result))

    get_tasks.short_description = 'Solutions'
    get_tasks.allow_tags = True

    def get_code_skills(self, obj):
        return obj.code_skills_rating

    get_code_skills.short_description = "Code skills"

    def get_code_design(self, obj):
        return obj.code_design_rating

    get_code_skills.short_description = "Code design"

    def get_fit_attitude(self, obj):
        return obj.fit_attitude_rating

    get_fit_attitude.short_description = "Fit attitude"

    def has_change_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True
