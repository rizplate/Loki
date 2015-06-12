from django.conf import settings
from django.db import IntegrityError
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import CheckIn, Student, Lecture, Course
from .serializers import (UpdateStudentSerializer, StudentNameSerializer,
                          LectureSerializer, CheckInSerializer, CourseSerializer)
from .premissions import IsStudent


@csrf_exempt
@require_POST
def set_check_in(request):
    mac = request.POST['mac']
    token = request.POST['token']

    if settings.CHECKIN_TOKEN != token:
        return HttpResponse(status=511)

    student = Student.objects.filter(mac__iexact=mac).first()
    if not student:
        student = None
    try:
        check_in = CheckIn(mac=mac, student=student)
        check_in.save()
    except IntegrityError:
        return HttpResponse(status=418)

    return HttpResponse(status=200)


@api_view(['GET'])
# @permission_classes((IsLecturer,))
def get_lectures(request):
    course_id = request.GET.get('course_id')
    lectures = Lecture.objects.filter(course_id=course_id)
    serializer = LectureSerializer(lectures, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
# @permission_classes((IsLecturer,))
def get_check_ins(request):
    student_id = request.GET.get('student_id')
    check_ins = CheckIn.objects.filter(student_id=student_id)
    serializer = CheckInSerializer(check_ins, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
# @permission_classes((IsLecturer,))
def get_courses(request):
    teacher = request.user.get_teacher()
    courses = teacher.teached_courses.all()
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class OnBoardStudent(APIView):
    permission_classes = (IsAuthenticated,)

    def make_student(self, baseuser):
        student = Student(baseuser_ptr_id=baseuser.id)
        student.save()
        student.__dict__.update(baseuser.__dict__)
        return student.save()

    def post(self, request, format=None):
        if not request.user.get_student():
            self.make_student(request.user)
            return Response(status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes((IsStudent,))
def student_update(request):
    student = request.user.get_student()
    serializer = UpdateStudentSerializer(student, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=400)


@api_view(['GET'])
# @permission_classes((IsLecturer,))
def get_students_for_course(request):
    course_id = request.GET.get('course_id')
    students = Course.objects.filter(id=course_id).student_set.all()
    serializer = StudentNameSerializer(students, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
