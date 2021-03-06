from import_export.admin import ImportExportActionModelAdmin

from django.contrib import admin, messages

from .modelresource import StudentResource, CourseAssignmentResource, WorkingAtResource
from .models import (Student, Course, CourseAssignment, Teacher, Lecture,
                     CheckIn, StudentNote, WorkingAt, Task, Solution,
                     Certificate, ProgrammingLanguage, GraderRequest,
                     RetestSolution, SourceCodeTest, BinaryFileTest, Week,
                     Material)

from .forms import FixJsonFieldDisplayInInheritedClassAdminForm


@admin.register(Student)
class StudentAdmin(ImportExportActionModelAdmin):
    resource_class = StudentResource

    list_display = [
        'id',
        'email',
        'first_name',
        'last_name',
        'mac',
        'github_account',
        'get_courses',
        'is_active'
    ]

    list_display_links = ['email']
    list_filter = ('courses', 'is_active')
    search_fields = ['email', 'first_name', 'last_name', 'mac', 'github_account']

    def get_courses(self, obj):
        return obj.courses.all()


@admin.register(StudentNote)
class StudentNoteAdmin(admin.ModelAdmin):
    list_display = [
        'assignment',
        'get_author',
        'post_time',
    ]

    list_display_links = ['assignment']

    def get_author(self, obj):
        return "{} {}".format(obj.author.first_name, obj.author.last_name)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'email',
        'first_name',
        'last_name',
        'mac',
    ]
    list_display_links = ['email']


@admin.register(CourseAssignment)
class CourseAssignmentAdmin(ImportExportActionModelAdmin):
    resource_class = CourseAssignmentResource

    list_display = [
        'user',
        'course',
        'group_time',
        'student_presence',
        'cv',
        'is_attending',
        'is_online',
    ]

    list_filter = ('course', 'group_time', 'is_attending', 'is_online')
    search_fields = ['user__first_name', 'user__last_name', 'user__email']
    list_display_links = ['user']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'english_name'
    ]

    list_display_links = ['name']


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = [
        'date',
        'course',
        'week'
    ]


@admin.register(CheckIn)
class CheckInAdmin(admin.ModelAdmin):
    list_display = [
        'date',
        'mac',
        'user'
    ]
    search_fields = ['mac', 'user__email']


class WorkingAtAdmin(ImportExportActionModelAdmin):
    resource_class = WorkingAtResource

    list_display = [
        'full_name',
        'company',
        'company_name',
        'course',
        'came_working',
        'location',
        'start_date',
        'end_date',
        'title',
        'description',
    ]
    search_fields = [
        'student__email',
        'company_name',
        'company__name',
        'student__first_name',
        'student__last_name',
    ]

    def full_name(self, obj):
        return obj.student.full_name

admin.site.register(WorkingAt, WorkingAtAdmin)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):

    list_display = [
        'name',
        'course',
        'week',
        'gradable',
        'submited_solutions'
    ]

    list_filter = [
        'course',
        'week',
    ]

    search_fields = ['course__name', 'name', 'week']

    def submited_solutions(self, task):
        return len(task.solution_set.all())


@admin.register(ProgrammingLanguage)
class ProgrammingLanguageAdmin(admin.ModelAdmin):

    list_display = [
        'name',
    ]

    list_filter = [
        'name',
    ]

    search_fields = ['name']


@admin.register(SourceCodeTest)
class SourceCodeTestAdmin(admin.ModelAdmin):
    list_display = [
        'task',
        'course',
        'language',
        'test_type',
    ]

    list_filter = [
        'language',
        'test_type',
    ]

    search_fields = ['task']

    def course(self, obj):
        return obj.task.course


@admin.register(BinaryFileTest)
class BinaryFileTestAdmin(admin.ModelAdmin):
    form = FixJsonFieldDisplayInInheritedClassAdminForm

    list_display = [
        'task',
        'language',
        'test_type',
    ]

    list_filter = [
        'language',
        'test_type',
    ]

    search_fields = ['task']


@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    form = FixJsonFieldDisplayInInheritedClassAdminForm

    def save_model(self, request, obj, form, change):
        if (obj.code is None or obj.code == "") and (obj.url is None or obj.url == ""):
            messages.set_level(request, messages.ERROR)
            messages.error(request, 'Url or Code should be given.')
            return
        else:
            obj.save()

    def get_solution_course(self, obj):
        return obj.task.course
    get_solution_course.short_description = "Course"
    get_solution_course.admin_order_field = "task__course"

    list_filter = [
        'status'
    ]

    readonly_fields = [
        'task',
        'student',
        'url',
        'code',
        'build_id',
        'check_status_location',
        'status',
        'test_output',
        'return_code',
    ]

    list_display = [
        'id',
        'task',
        'status',
        'student',
        'get_solution_course',
        'url',
    ]

    list_filter = [
        'task',
    ]

    search_fields = ['id', 'task__name', 'student__first_name']


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'assignment',
        'token',
    ]


@admin.register(GraderRequest)
class GraderRequestAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'request_info',
        'nonce',
    ]

    list_filter = [
        'request_info',
    ]

    search_fields = ['nonce']


@admin.register(RetestSolution)
class RetestSolutionAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'status',
        'date',
        'test_id',
        'tested_solutions_count',
    ]

    list_filter = [
        'status',
    ]

    search_fields = ['test_id']


@admin.register(Week)
class WeekAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'number'
    ]

    list_filter = [
        'number'
    ]

    search_fields = ['number']


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'title',
        'week',
        'course',
    ]

    list_filter = [
        'week'
    ]

    search_fields = ['course']
