from django.core.management import call_command
from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework.test import APIClient
from base_app.models import Company
from base_app.models import City

from education.models import Student, CheckIn, Course, Lecture, Teacher, CourseAssignment, StudentNote, WorkingAt
from hack_fmi.models import BaseUser
from hack_fmi.helper import date_increase, date_decrease
from loki.settings import CHECKIN_TOKEN


class CheckInTest(TestCase):

    def setUp(self):
        self.student = Student.objects.create(
            email='sten@abv.bg',
            mac="12-34-56-78-9A-BC",
        )
        self.teacher = Teacher.objects.create(
            email='teach@teach.bg'
        )
        self.student_no_mac = Student.objects.create(
            email='rado@abv.bg',
        )
        self.course = Course.objects.create(
            description='Test',
            name='Test',
            application_until=date_decrease(30),
            SEO_description='Test',
            SEO_title='Test',
            url='haskell-12',
            start_time=date_decrease(29),
            end_time=date_decrease(2),
        )

        self.course_assignment = CourseAssignment.objects.create(
            group_time=1,
            course=self.course,
            user=self.student,
        )

        self.check_in_on_start = CheckIn.objects.create(
            mac="12-34-56-78-9A-BE",
            student=self.student,
        )
        self.check_in_on_start.date = date_decrease(29)
        self.check_in_on_start.save()

        self.check_in_after_start = CheckIn.objects.create(
            mac="12-34-56-78-9A-BE",
            student=self.student,
        )
        self.check_in_after_start.date = date_decrease(20)
        self.check_in_after_start.save()

        self.check_in_on_end = CheckIn.objects.create(
            mac="12-34-56-78-9A-BE",
            student=self.student,
        )
        self.check_in_on_end.date = date_decrease(2)
        self.check_in_on_end.save()

        self.check_in_after_course = CheckIn.objects.create(
            mac="12-34-56-78-9A-BE",
            student=self.student,
        )
        self.check_in_after_course.date = date_decrease(1)
        self.check_in_after_course.save()

        self.check_in_before_course = CheckIn.objects.create(
            mac="12-34-56-78-9A-BE",
            student=self.student,
        )
        self.check_in_before_course.date = date_decrease(30)
        self.check_in_before_course.save()

    def test_check_in_with_mac_and_user(self):
        data = {
            'mac': '12-34-56-78-9A-BC',
            'token': CHECKIN_TOKEN,
        }
        url = reverse('education:set_check_in')
        self.client.post(url, data, format='json')
        self.assertIn(self.student.mac, CheckIn.objects.get(mac='12-34-56-78-9A-BC').student.mac)

    def test_check_in_with_mac_and_no_user(self):
        data = {
            'mac': '12-34-56-78-9A-BA',
            'token': CHECKIN_TOKEN,
        }
        url = reverse('education:set_check_in')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.client.post(url, data, format='json')

    def test_check_macs_command(self):
        data = {
            'mac': '12-34-56-78-9A-BA',
            'token': CHECKIN_TOKEN,
        }
        url = reverse('education:set_check_in')
        self.client.post(url, data, format='json')
        self.assertIsNone(CheckIn.objects.get(mac='12-34-56-78-9A-BA').student)
        self.student_no_mac.mac = '12-34-56-78-9A-BA'
        self.student_no_mac.save()
        call_command('check_macs')
        self.assertEqual(CheckIn.objects.get(mac='12-34-56-78-9A-BA').student, self.student_no_mac)

    def test_get_check_ins_for_specific_course(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.teacher)
        data = {
            'student_id': self.student.id,
            'course_id': self.course.id
        }
        url = reverse('education:get_check_ins')
        response = self.client.get(url, data, format='json')
        check_ins = CheckIn.objects.filter(student_id=self.student.id,
                                           date__gte=self.course.start_time,
                                           date__lte=self.course.end_time)
        self.assertEqual(len(response.data), len(check_ins))


class AuthenticationTests(TestCase):

    def setUp(self):
        self.user = BaseUser.objects.create(
            email="test@test.bg",
            first_name="Tester",
            last_name="Testov"
        )

    def test_onboard_student(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        student_count = Student.objects.count()
        baseuser_count = BaseUser.objects.count()
        url = reverse('education:onboard_student')
        response = self.client.post(url, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Student.objects.count() - 1, student_count)
        self.assertEqual(BaseUser.objects.count(), baseuser_count)

        self.assertEqual(
            BaseUser.objects.first().email,
            Student.objects.first().email
        )


class UpdateStudentsTests(TestCase):

    def setUp(self):
        self.student = Student.objects.create(
            email='sten@abv.bg',
            mac="12-34-56-78-9A-BC",
        )

    def test_student_update(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.student)
        url = reverse('education:student_update')
        data = {'mac': '01:23:45:67:ab:ab'}
        self.client.patch(url, data, format='json')

        student = Student.objects.filter(email="sten@abv.bg").first()
        self.assertEqual(student.mac, data['mac'])


class TeachersAPIsTests(TestCase):

    def setUp(self):
        self.course1 = Course.objects.create(
            name="Java",
            application_until=date_decrease(30),
            url="https://hackbulgaria.com/course/haskell-1/",
            start_time=date_decrease(29),
            end_time=date_decrease(2),
        )
        self.course2 = Course.objects.create(
            name="Python",
            application_until=date_decrease(30),
            url="https://hackbulgaria.com/course/haskell-2/",
            start_time=date_decrease(29),
            end_time=date_decrease(2),
        )
        self.course3 = Course.objects.create(
            name="Python3",
            application_until=date_decrease(30),
            url="https://hackbulgaria.com/course/haskell-3/",
            start_time=date_decrease(29),
            end_time=date_decrease(2),
        )
        Lecture.objects.create(
            course=self.course1,
            date=date_decrease(8)
        )
        Lecture.objects.create(
            course=self.course1,
            date=date_decrease(10)
        )
        self.teacher = Teacher.objects.create(
            email="ivo@ivo.bg",
        )
        self.teacher.teached_courses.add(self.course1)
        self.teacher.save()
        self.teacher.teached_courses.add(self.course2)
        self.teacher.save()
        self.student = Student.objects.create(
            email="stud@abv.bg",
            mac="60:67:20:cc:b1:62"
        )
        self.course_assignment = CourseAssignment.objects.create(
            user=self.student,
            course=self.course2,
            group_time=1
        )
        self.course_assignment2 = CourseAssignment.objects.create(
            user=self.student,
            course=self.course3,
            group_time=1
        )

    def test_get_courses_api(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.teacher)
        course_count = self.teacher.teached_courses.count()
        url = reverse('education:get_courses')
        response = self.client.get(url, format='json')
        self.assertEqual(course_count, len(response.data))

    def test_get_lectures(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.teacher)
        data = {'course_id': self.course1.id}
        url = reverse('education:get_lectures')
        response = self.client.get(url, data, format='json')
        lectures = Lecture.objects.filter(course=self.course1)
        self.assertEqual(len(response.data), len(lectures))

    def test_create_student_note_valid_data(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.teacher)
        data = {
            'ca_id': self.course_assignment.id,
            'text': 'Very good student!'
        }
        url = reverse('education:create_student_note')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        note = StudentNote.objects.filter(assignment=self.course_assignment).first()
        self.assertEqual(note.text, 'Very good student!')

    def test_create_student_note_invalid_teacher(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.teacher)
        data = {
            'ca_id': self.course_assignment2.id,
            'text': 'Very good student!'
        }
        url = reverse('education:create_student_note')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 401)
        note = StudentNote.objects.filter(assignment=self.course_assignment2).first()
        self.assertIsNone(note)


class CheckPresenceTests(TestCase):
    def setUp(self):
        self.course1 = Course.objects.create(
            name="Java",
            application_until=date_decrease(31),
            url="https://hackbulgaria.com/course/haskell-1/",
            start_time=date_decrease(30),
            end_time=date_increase(30)
        )
        self.course2 = Course.objects.create(
            name="Python",
            application_until=date_decrease(31),
            url="https://hackbulgaria.com/course/haskell-2/",
            start_time=date_decrease(30),
            end_time=date_increase(30)
        )
        Lecture.objects.create(
            course=self.course1,
            date=date_decrease(1)
        )
        Lecture.objects.create(
            course=self.course1,
            date=date_decrease(2)
        )
        Lecture.objects.create(
            course=self.course1,
            date=date_decrease(3)
        )

        self.student = Student.objects.create(
            email="stud@abv.bg",
            mac="60:67:20:cc:b1:62"
        )
        self.course_assignment = CourseAssignment.objects.create(
            user=self.student,
            course=self.course1,
            group_time=1
        )
        self.check_in_1 = CheckIn.objects.create(
            mac="12:34:56:78:9A:BE",
            student=self.student,
        )
        self.check_in_1.date = date_decrease(1)
        self.check_in_1.save()
        self.check_in_2 = CheckIn.objects.create(
            mac="12:34:56:78:9A:BE",
            student=self.student,
        )
        self.check_in_2.date = date_decrease(2)
        self.check_in_2.save()

    def test_command(self):
        self.assertIsNone(self.course_assignment.student_presence)
        call_command('check_presence')
        ca = CourseAssignment.objects.get(id=self.course_assignment.id)
        self.assertEqual(ca.student_presence, 67)


class DropStudentTests(TestCase):

    def setUp(self):
        self.course1 = Course.objects.create(
            name="Java",
            application_until="2015-06-20",
            url="https://hackbulgaria.com/course/haskell-1/",
            start_time=date_decrease(30),
            end_time=date_increase(30)
        )
        self.student = Student.objects.create(
            email="stud@abv.bg",
            mac="60:67:20:cc:b1:62"
        )
        self.course_assignment = CourseAssignment.objects.create(
            user=self.student,
            course=self.course1,
            group_time=1,
            is_attending=True
        )
        self.teacher = Teacher.objects.create(
            email="ivo@ivo.bg",
        )
        self.teacher.teached_courses.add(self.course1)
        self.teacher.save()

    def test_drop_student_who_is_attending(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.teacher)
        data = {
            'ca_id': self.course_assignment.id,
            'is_attending': False
        }
        url = reverse('education:drop_student')
        self.assertTrue(self.course_assignment.is_attending)
        self.client.patch(url, data, format='json')
        cass = CourseAssignment.objects.get(id=self.course_assignment.id)
        self.assertFalse(cass.is_attending)


class CheckMacsTests(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            email='sten@abv.bg',
            mac="12:34:56:78:9A:BC",
        )
        self.student_no_mac = Student.objects.create(
            email='rado@abv.bg',
        )
        self.check_1 = CheckIn.objects.create(
            mac="12:34:56:78:9A:BE",
        )
        self.check_1.date = date_decrease(1)
        self.check_1.save()

        self.check_2 = CheckIn.objects.create(
            mac="12:34:56:78:9A:BE",
        )
        self.check_2.date = date_decrease(2)
        self.check_2.save()

        self.check_3 = CheckIn.objects.create(
            mac="12:34:56:78:9A:BE",
        )
        self.check_3.date = date_decrease(3)
        self.check_3.save()

    def test_student_enters_mac(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.student_no_mac)
        data = {'mac': '12:34:56:78:9A:BE'}
        url = reverse('education:student_update')
        self.client.patch(url, data, format='json')
        ch = CheckIn.objects.filter(mac='12:34:56:78:9A:BE').first()
        self.assertEqual(ch.student, self.student_no_mac)


class TestGetCompanies(TestCase):

    def setUp(self):
        Company.objects.create(
            name="com"
        )
        Company.objects.create(
            name="coma"
        )

    def test_get_all_companies(self):
        count = Company.objects.count()
        url = reverse('education:get_companies')
        response = self.client.get(url, format='json')
        self.assertEqual(count, len(response.data))


class TestGetCities(TestCase):

    def setUp(self):
        City.objects.create(
            name="com"
        )
        City.objects.create(
            name="coma"
        )

    def test_get_all_companies(self):
        count = City.objects.count()
        url = reverse('education:get_cities')
        response = self.client.get(url, format='json')
        self.assertEqual(count, len(response.data))


class WorkingAtTests(TestCase):

    def setUp(self):
        self.student = Student.objects.create(
            email='sten@abv.bg',
            mac="12:34:56:78:9A:BC",
        )
        self.company = Company.objects.create(
            name="HackBulgaria"
        )
        self.city = City.objects.create(
            name="Sofia"
        )
        self.course = Course.objects.create(
            name="Java",
            application_until=date_decrease(30),
            url="https://hackbulgaria.com/course/haskell-1/",
            start_time=date_decrease(29),
            end_time=date_decrease(2),
        )
        self.course_assignment = CourseAssignment.objects.create(
            group_time=1,
            course=self.course,
            user=self.student,
        )

    def test_post_workingat_creates_instance(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.student)
        url = reverse('education:working_at')
        data = {
            'company_name': "Hackbulgaria",
            'location': self.city.id,
            'start_date': date_decrease(30),
            'title': 'Developer',
            'course_assignment': self.course_assignment.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.data['location_full']), 2)
        self.assertEqual(len(response.data['course_assignment_full']), 3)

    def test_patch_workingat_updates_instance(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.student)
        work = WorkingAt.objects.create(
            student=self.student,
            company_name='HackBulgaria',
            location=self.city,
            start_date=date_decrease(30),
            title='Developer',
            course_assignment=self.course_assignment
        )
        city2 = City.objects.create(
            name='Plovdiv'
        )
        url = reverse('education:working_at')
        data = {
            'working_at_id': work.id,
            'location': city2.id
        }
        city_before = WorkingAt.objects.first().location.name
        self.client.patch(url, data, format='json')
        city_after = WorkingAt.objects.first().location.name
        self.assertEqual(city_before, self.city.name)
        self.assertEqual(city_after, city2.name)
