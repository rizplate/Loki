from unittest import mock

from test_plus.test import TestCase
from django.core.management import call_command
from datetime import datetime, timedelta

from loki.seed.factories import (
    BaseUserFactory,
    CourseFactory,
    CourseAssignmentFactory,
    LectureFactory,
    CheckInFactory,
    StudentFactory,
    TaskFactory,
    SolutionFactory
)

from loki.education.models import (
    Lecture,
    CheckIn,
    Certificate,
    Solution
)


class CalculatePresenceTests(TestCase):

    def setUp(self):
        self.student1 = StudentFactory()
        self.student1.is_active = True
        self.student1.set_password(BaseUserFactory.password)
        self.student1.save()

        self.student2 = StudentFactory()
        self.student2.is_active = True
        self.student2.set_password(BaseUserFactory.password)
        self.student2.save()

        self.course = CourseFactory(start_time=datetime.now().date() - timedelta(days=10),
                                    end_time=datetime.now().date() + timedelta(days=10))
        self.course_assignment = CourseAssignmentFactory(course=self.course,
                                                         user=self.student1)
        self.course_assignment2 = CourseAssignmentFactory(course=self.course,
                                                          user=self.student2)

        LectureFactory(course=self.course,
                       date=datetime.now().date() - timedelta(days=9))

        LectureFactory(course=self.course,
                       date=datetime.now().date() - timedelta(days=7))

        LectureFactory(course=self.course,
                       date=datetime.now().date() - timedelta(days=5))

        LectureFactory(course=self.course,
                       date=datetime.now().date() - timedelta(days=3))

    def test_calculate_presence_when_student_havenot_checkins_for_course(self):
        self.assertEqual(self.course_assignment.student_presence, 0)
        self.assertEqual(self.course_assignment2.student_presence, 0)

        call_command('calculate_presence')

        self.assertEqual(self.course_assignment.student_presence, 0)
        self.assertEqual(self.course_assignment2.student_presence, 0)

    def test_calculate_presence_when_student_have_checkins_for_other_dates(self):
        check_in1 = CheckInFactory(mac=self.student1.mac,
                                   user=self.student1)
        check_in1.date = datetime.now().date() - timedelta(days=8)
        check_in1.save()
        check_in2 = CheckInFactory(mac=self.student1.mac,
                                   user=self.student1)
        check_in2.date = datetime.now().date() - timedelta(days=6)
        check_in2.save()

        self.assertEqual(self.course_assignment.student_presence, 0)
        self.assertEqual(4, Lecture.objects.filter(course=self.course).count())
        self.assertEqual(2, CheckIn.objects.get_user_dates(user=self.student1, course=self.course).count())

        call_command('calculate_presence')

        self.assertEqual(self.course_assignment.student_presence, 0)

    def test_calculate_presence_when_student_have_checkins_for_course_lecture(self):
        check_in1 = CheckInFactory(mac=self.student1.mac,
                                   user=self.student1)
        check_in1.date = datetime.now().date() - timedelta(days=9)
        check_in1.save()
        check_in2 = CheckInFactory(mac=self.student1.mac,
                                   user=self.student1)
        check_in2.date = datetime.now().date() - timedelta(days=7)
        check_in2.save()

        check_in3 = CheckInFactory(mac=self.student2.mac,
                                   user=self.student2)
        check_in3.date = datetime.now().date() - timedelta(days=5)
        check_in3.save()
        check_in4 = CheckInFactory(mac=self.student2.mac,
                                   user=self.student2)
        check_in4.date = datetime.now().date() - timedelta(days=3)
        check_in4.save()
        check_in5 = CheckInFactory(mac=self.student2.mac,
                                   user=self.student2)
        check_in5.date = datetime.now().date() - timedelta(days=7)
        check_in5.save()

        self.assertEqual(self.course_assignment.student_presence, 0)
        self.assertEqual(4, Lecture.objects.filter(course=self.course).count())
        self.assertEqual(2, CheckIn.objects.get_user_dates(user=self.student1, course=self.course).count())
        self.assertEqual(3, CheckIn.objects.get_user_dates(user=self.student2, course=self.course).count())

        call_command('calculate_presence')
        self.course_assignment.refresh_from_db()
        self.assertEqual(self.course_assignment.student_presence, 50)

        self.course_assignment2.refresh_from_db()
        self.assertEqual(self.course_assignment2.student_presence, 75)


class GenerateCertificatesTests(TestCase):
    def setUp(self):
        now = datetime.now()
        self.student = StudentFactory()
        self.course = CourseFactory(start_time=now.date() - timedelta(days=10),
                                    end_time=now.date() + timedelta(days=10),
                                    generate_certificates_until=now.date() + timedelta(days=10))
        self.course_assignment = CourseAssignmentFactory(course=self.course,
                                                         user=self.student)

    def test_certificate_is_generated_for_student(self):
        self.assertEqual(0, Certificate.objects.count())

        call_command('generate_certificates')

        self.assertEqual(1, Certificate.objects.count())

        cert = Certificate.objects.first()
        self.assertEqual(cert, self.course_assignment.certificate)


class RegradePendingSolutionsTests(TestCase):
    def setUp(self):
        self.student = StudentFactory()
        self.course = CourseFactory()

        self.task = TaskFactory(course=self.course)
        self.solution = SolutionFactory(student=self.student,
                                        task=self.task,
                                        status=Solution.PENDING)

    @mock.patch('loki.education.tasks.submit_solution', side_effect=lambda *args, **kwargs: None)
    def test_regrade_pending_solution_submits_pending_solutions(self, mock):
        call_command('regrade_pending_solutions')

        self.solution.refresh_from_db()
        self.assertEqual(Solution.SUBMITED, self.solution.status)