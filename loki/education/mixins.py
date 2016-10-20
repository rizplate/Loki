from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from loki.education.models import Course, CourseAssignment


class BaseUserPassesTestMixin(UserPassesTestMixin):
    def test_func(self):
        return True


class DashboardPermissionMixin(BaseUserPassesTestMixin):
    raise_exception = True
    requires_login = False

    def test_func(self):
        if not self.request.user.is_authenticated():
            self.requires_login = True
            return False

        if not (self.request.user.get_student() or \
                self.request.user.get_teacher() or \
                self.request.user.is_superuser):
            return False

        return True and super().test_func()

    def handle_no_permission(self):
        if self.requires_login:
            return redirect_to_login(
                self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

        return super().handle_no_permission()


class CannotSeeOthersCoursesDashboardsMixin(BaseUserPassesTestMixin):
    def test_func(self):
        course_id = self.kwargs.get('course')
        course = Course.objects.filter(id=course_id).first()
        qs = CourseAssignment.objects.filter(user=self.request.user, course=course)

        if not qs.exists():
            return False

        self.course = course
        return True and super().test_func()
