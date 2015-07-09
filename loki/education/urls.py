from django.conf.urls import url
from education.views import (set_check_in, get_lectures, get_check_ins,
                             get_courses, OnBoardStudent, student_update, get_students_for_course, get_cas_for_course,
                             create_student_note, drop_student)


urlpatterns = [
    url(r'^api/set-check-in/$', set_check_in, name='set_check_in'),
    url(r'^api/get-lectures/$', get_lectures, name='get_lectures'),
    url(r'^api/get-check-ins/$', get_check_ins, name='get_check_ins'),
    url(r'^api/get-courses/$', get_courses, name='get_courses'),
    url(r'^api/student-update/$', student_update, name='student_update'),
    url(r'^api/onboard-student/$', OnBoardStudent.as_view(), name='onboard_student'),
    url(r'^api/get-students-for-course/$', get_students_for_course, name='get_students_for_course'),
    url(r'^api/get-cas-for-course/$', get_cas_for_course, name='get_ca_for_course'),
    url(r'^api/create-student_note/$', create_student_note, name='create_student_note'),
    url(r'^api/drop-student/$', drop_student, name='drop_student'),
]
