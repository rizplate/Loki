import factory
from django.utils import timezone
from datetime import datetime, timedelta
from faker import Factory

from loki.base_app import models as base_app_models
from loki.hack_fmi import models as hack_fmi_models
from loki.education import models as education_models
from loki.website import models as website_models
from loki.applications import models as application_models
from loki.interview_system import models as interview_models

from loki.hack_fmi.helper import date_increase, date_decrease
faker = Factory.create()


class CompanyFactory(factory.DjangoModelFactory):
    class Meta:
        model = base_app_models.Company

    name = factory.Sequence(lambda n: '{}-{}'.format(faker.word(), n))
    logo_url = factory.LazyAttribute(lambda _: faker.url())
    logo = factory.django.ImageField(color='blue')
    jobs_link = factory.LazyAttribute(lambda _: faker.url())


class PartnerFactory(factory.DjangoModelFactory):
    class Meta:
        model = base_app_models.Partner

    company = factory.SubFactory(CompanyFactory)
    description = factory.LazyAttribute(lambda _: faker.text())
    facebook = factory.LazyAttribute(lambda _: faker.url())
    is_active = factory.LazyAttribute(lambda _: faker.boolean())
    money_spent = factory.LazyAttribute(lambda _: faker.random_int())
    ordering = factory.LazyAttribute(lambda _: faker.random_int())
    twitter = factory.LazyAttribute(lambda _: faker.url())
    website = factory.LazyAttribute(lambda _: faker.url())
    video_presentation = factory.LazyAttribute(lambda _: faker.url())


class GeneralPartnerFactory(factory.DjangoModelFactory):
    class Meta:
        model = base_app_models.GeneralPartner

    partner = factory.SubFactory(PartnerFactory)


class HostingPartnerFactory(factory.DjangoModelFactory):
    class Meta:
        model = base_app_models.HostingPartner

    partner = factory.SubFactory(PartnerFactory)


class CityFactory(factory.DjangoModelFactory):
    class Meta:
        model = base_app_models.City

    name = factory.Sequence(lambda n: 'city {}'.format(n))


class EducationPlaceFactory(factory.DjangoModelFactory):
    class Meta:
        model = base_app_models.EducationPlace

    name = factory.Sequence(lambda n: '{}{}'.format(faker.name(), n))
    city = factory.SubFactory(CityFactory)


class SchoolFactory(EducationPlaceFactory):
    class Meta:
        model = base_app_models.School


class AcademyFactory(EducationPlaceFactory):
    class Meta:
        model = base_app_models.Academy


class UniversityFactory(EducationPlaceFactory):
    class Meta:
        model = base_app_models.University


class FacultyFactory(factory.DjangoModelFactory):
    class Meta:
        model = base_app_models.Faculty

    university = factory.SubFactory(UniversityFactory)
    name = factory.Sequence(lambda n: '{}{}'.format(faker.name(), n))
    abbreviation = factory.Sequence(lambda n: '{}{}'.format(faker.random_letter(), n))


class SubjectFactory(factory.DjangoModelFactory):
    class Meta:
        model = base_app_models.Subject

    faculty = factory.SubFactory(FacultyFactory)
    name = factory.Sequence(lambda n: '{}{}'.format(faker.name(), n))


class BaseUserFactory(factory.DjangoModelFactory):
    class Meta:
        model = base_app_models.BaseUser

    password = 'ivoepanda'
    first_name = factory.LazyAttribute(lambda _: faker.first_name())
    last_name = factory.LazyAttribute(lambda _: faker.last_name())
    email = factory.Sequence(lambda n: '{}{}'.format(n, faker.email()))
    birth_place = factory.SubFactory(CityFactory)

    github_account = factory.LazyAttribute(lambda _: faker.url())
    linkedin_account = factory.LazyAttribute(lambda _: faker.url())
    twitter_account = factory.LazyAttribute(lambda _: faker.url())
    description = factory.LazyAttribute(lambda _: faker.text())

    studies_at = factory.LazyAttribute(lambda _: faker.text(max_nb_chars=100))
    works_at = factory.LazyAttribute(lambda _: faker.text(max_nb_chars=100))

    avatar = factory.django.ImageField(color='blue')
    full_image = factory.django.ImageField(color='blue')

    created_at = datetime.now()


class EducationInfoFactory(factory.DjangoModelFactory):
    class Meta:
        model = base_app_models.EducationInfo

    user = factory.SubFactory(BaseUserFactory)
    place = factory.SubFactory(EducationPlaceFactory)

    start_date = factory.LazyAttribute(lambda _: faker.date_time())
    end_date = factory.LazyAttribute(lambda _: faker.date_time())
    created_at = factory.LazyAttribute(lambda _: faker.date_time())
    updated_at = factory.LazyAttribute(lambda _: faker.date_time())

    faculty = factory.SubFactory(FacultyFactory)
    subject = factory.SubFactory(SubjectFactory)


class BaseUserRegisterTokenFactory(factory.DjangoModelFactory):
    class Meta:
        model = base_app_models.BaseUserRegisterToken

    user = factory.SubFactory(BaseUserFactory)
    token = factory.Sequence(lambda n: '{}{}'.format(faker.word(), n))


class BaseUserPasswordResetTokenFactory(factory.DjangoModelFactory):
    class Meta:
        model = base_app_models.BaseUserPasswordResetToken

    user = factory.SubFactory(BaseUserFactory)
    token = factory.Sequence(lambda n: '{}{}'.format(faker.text(max_nb_chars=20), n))


class SkillFactory(factory.DjangoModelFactory):
    class Meta:
        model = hack_fmi_models.Skill

    name = factory.Sequence(lambda n: '{}{}'.format(faker.text(max_nb_chars=25), n))


class StudentFactory(BaseUserFactory):
    class Meta:
        model = education_models.Student

    mac = factory.LazyAttribute(lambda _: faker.mac_address())
    phone = factory.LazyAttribute(lambda _: faker.text(max_nb_chars=20))
    skype = factory.LazyAttribute(lambda _: faker.text(max_nb_chars=20))
    looking_for_job = False


class CourseFactory(factory.DjangoModelFactory):
    class Meta:
        model = education_models.Course

    git_repository = factory.LazyAttribute(lambda _: faker.word())
    name = factory.Sequence(lambda n: '{}{}'.format(faker.name(), n))
    partner = factory.RelatedFactory(PartnerFactory)

    end_time = faker.date_time()
    start_time = faker.date_time()
    deadline_date = datetime.now().date()

    fb_group = faker.url()
    generate_certificates_until = faker.date()


class CourseAssignmentFactory(factory.DjangoModelFactory):
    class Meta:
        model = education_models.CourseAssignment

    course = factory.SubFactory(CourseFactory)
    user = factory.SubFactory(StudentFactory)
    cv = faker.file_name(category=None, extension=None)
    favourite_partners = factory.RelatedFactory(PartnerFactory)
    group_time = int(faker.random_element(elements=('1', '2')))
    is_attending = True
    student_presence = 0
    is_online = faker.boolean()


class TeacherFactory(factory.DjangoModelFactory):
    class Meta:
        model = education_models.Teacher

    mac = faker.mac_address()
    phone = faker.text(max_nb_chars=20)
    signature = factory.django.ImageField()
    teached_courses = factory.RelatedFactory(CourseFactory)


class StudentWithAssignmentFactory(StudentFactory):

    courses = factory.RelatedFactory(CourseAssignmentFactory)


class CompetitorFactory(BaseUserFactory):
    class Meta:
        model = hack_fmi_models.Competitor

    is_vegetarian = faker.boolean()
    known_skills = factory.RelatedFactory(SkillFactory)
    faculty_number = faker.random_number()
    shirt_size = faker.random_element(elements=('1', '2', '3', '4'))
    needs_work = faker.boolean()
    social_links = faker.text()
    registered = faker.boolean()


class SeasonFactory(factory.DjangoModelFactory):
    class Meta:
        model = hack_fmi_models.Season

    name = factory.Sequence(lambda n: "season{}".format(n))
    topic = faker.word()
    front_page = faker.paragraph()
    min_team_members_count = int(faker.random_element(elements=('1', '2')))
    max_team_members_count = int(faker.random_element(elements=('7', '8')))
    sign_up_deadline = faker.date()
    # Increase with 20 days form date.today()
    make_team_dead_line = date_increase(10)
    # In order to be able to pick up mentor in date.today(),
    # the pick up period must have started ==> date_decrease
    mentor_pick_start_date = date_decrease(20)
    mentor_pick_end_date = date_increase(20)
    max_mentor_pick = faker.random_element(elements=('3', '4'))
    is_active = faker.boolean(chance_of_getting_true=0)


class HackFmiPartnerFactory(factory.DjangoModelFactory):
    class Meta:
        model = hack_fmi_models.Partner

    name = faker.name()
    season = factory.RelatedFactory(SeasonFactory)


class RoomFactory(factory.DjangoModelFactory):
    class Meta:
        model = hack_fmi_models.Room

    number = factory.Sequence(lambda n: n)
    season = factory.SubFactory(SeasonFactory)
    capacity = faker.random_number(digits=1)


class MentorFactory(factory.DjangoModelFactory):
    class Meta:
        model = hack_fmi_models.Mentor

    name = factory.Sequence(lambda n: "mentor{}".format(n))
    description = faker.text()
    picture = factory.django.ImageField()
    seasons = factory.RelatedFactory(SeasonFactory)
    from_company = factory.SubFactory(HackFmiPartnerFactory)
    order = faker.random_number()


class TeamFactory(factory.DjangoModelFactory):
    class Meta:
        model = hack_fmi_models.Team

    name = factory.Sequence(lambda n: faker.word() + str(n))
    mentors = factory.RelatedFactory(MentorFactory)
    technologies = factory.RelatedFactory(SkillFactory)
    idea_description = faker.text()
    repository = faker.url()
    season = factory.SubFactory(SeasonFactory)
    need_more_members = faker.boolean()
    room = factory.SubFactory(RoomFactory)
    place = faker.random_number(digits=1)


class TeamMembershipFactory(factory.DjangoModelFactory):
    class Meta:
        model = hack_fmi_models.TeamMembership

    competitor = factory.SubFactory(CompetitorFactory)
    team = factory.SubFactory(TeamFactory)
    is_leader = faker.boolean()


class TeamMentorshipFactory(factory.DjangoModelFactory):
    class Meta:
        model = hack_fmi_models.TeamMentorship

    mentor = factory.SubFactory(MentorFactory)
    team = factory.SubFactory(TeamFactory)


class TeamWithCompetitor(TeamFactory):
    class Meta:
        exclude = ('competitor')

    competitor = factory.SubFactory(CompetitorFactory)
    members = factory.RelatedFactory(TeamMembershipFactory,
                                     'team',
                                     competitor=competitor)


class CertificateFactory(factory.DjangoModelFactory):
    class Meta:
        model = education_models.Certificate

    assignment = factory.SubFactory(CourseAssignmentFactory)
    token = faker.uuid4()


class CheckInFactory(factory.DjangoModelFactory):
    class Meta:
        model = education_models.CheckIn

    mac = factory.LazyAttribute(lambda _: faker.mac_address())
    user = factory.SubFactory(BaseUserFactory)
    date = faker.date()


class WeekFactory(factory.DjangoModelFactory):
    class Meta:
        model = education_models.Week

    number = faker.random_number()


class LectureFactory(factory.DjangoModelFactory):
    class Meta:
        model = education_models.Lecture

    course = factory.SubFactory(CourseFactory)
    week = factory.SubFactory(WeekFactory)
    date = faker.date_time()


class WorkingAtFactory(factory.DjangoModelFactory):
    class Meta:
        model = education_models.WorkingAt

    student = factory.SubFactory(StudentFactory)
    company = factory.SubFactory(CompanyFactory)
    location = factory.SubFactory(CityFactory)
    course = factory.SubFactory(CourseFactory)
    came_working = faker.boolean(chance_of_getting_true=0)
    company_name = faker.company()
    start_date = faker.date_time()
    end_date = faker.date_time()
    title = faker.word()
    description = faker.text()


class TaskFactory(factory.DjangoModelFactory):
    class Meta:
        model = education_models.Task

    course = factory.SubFactory(CourseFactory)
    description = factory.\
        Sequence(lambda n: 'https://github.com/task{}/'.format(n))
    is_exam = faker.boolean(chance_of_getting_true=0)
    name = factory.LazyAttribute(lambda _: faker.word())
    week = faker.random_number(digits=1)
    gradable = faker.boolean(chance_of_getting_true=100)


class ProgrammingLanguageFactory(factory.DjangoModelFactory):
    class Meta:
        model = education_models.ProgrammingLanguage

    name = faker.word()


class TestFactory(factory.DjangoModelFactory):
    class Meta:
        model = education_models.Test

    task = factory.RelatedFactory(TaskFactory)
    language = factory.SubFactory(ProgrammingLanguageFactory)


class SourceCodeTestFactory(TestFactory):
    class Meta:
        model = education_models.SourceCodeTest

    code = faker.text()


class BinaryFileTestFactory(TestFactory):
    class Meta:
        model = education_models.BinaryFileTest

    file = faker.file_name(category=None, extension=None)


class SolutionFactory(factory.DjangoModelFactory):
    class Meta:
        model = education_models.Solution

    task = factory.SubFactory(TaskFactory)
    student = factory.SubFactory(StudentFactory)

    '''Non-gradable tasks require a github url'''

    url = factory.\
        Sequence(lambda n: 'https://github.com/zad{}/solution.py'.format(n))
    code = faker.text()
    status = faker.random_element(elements=(0, 1, 2, 3, 4, 5, 6))


class StudentNoteFactory(factory.DjangoModelFactory):
    class Meta:
        model = education_models.StudentNote

    text = faker.text()
    assignment = factory.SubFactory(CourseAssignmentFactory)
    author = factory.SubFactory(TeacherFactory)
    post_time = faker.date_time()


class GraderRequestFactory(factory.DjangoModelFactory):
    class Meta:
        model = education_models.GraderRequest

    request_info = faker.text(max_nb_chars=140)
    nonce = faker.random_number(digits=3)


class MaterialFactory(factory.DjangoModelFactory):
    class Meta:
        model = education_models.Material

    course = factory.SubFactory(CourseFactory)
    week = factory.SubFactory(WeekFactory)
    description = faker.text(max_nb_chars=200)
    title = faker.word()


class SnippetFactory(factory.DjangoModelFactory):
    class Meta:
        model = website_models.Snippet

    label = faker.text(max_nb_chars=80)
    text = faker.text()


class CourseDescriptionFactory(factory.DjangoModelFactory):
    class Meta:
        model = website_models.CourseDescription

    course = factory.SubFactory(CourseFactory)
    custom_logo = factory.django.ImageField()
    url = factory.LazyAttribute(lambda _: faker.slug())
    video_image = factory.django.ImageField()
    blog_article = faker.text(max_nb_chars=255)

    course_intensity = faker.random_number()
    course_days = faker.text(max_nb_chars=255)
    paid_course = faker.boolean(chance_of_getting_true=0)
    course_summary = faker.text()
    teacher_preview = faker.text()
    realization = faker.text()
    price_text = faker.text()
    address = faker.text(max_nb_chars=255)
    SEO_description = faker.text(max_nb_chars=255)
    SEO_title = faker.text(max_nb_chars=255)


class InvitationFactory(factory.DjangoModelFactory):
    class Meta:
        model = hack_fmi_models.Invitation

    team = factory.SubFactory(TeamFactory)
    competitor = factory.SubFactory(CompetitorFactory)


class SeasonCompetitorInfoFactory(factory.DjangoModelFactory):
    class Meta:
        model = hack_fmi_models.SeasonCompetitorInfo

    season = factory.SubFactory(SeasonFactory)
    competitor = factory.SubFactory(CompetitorFactory)


class ApplicationInfoFactory(factory.DjangoModelFactory):
    class Meta:
        model = application_models.ApplicationInfo

    course = factory.SubFactory(CourseDescriptionFactory)
    start_date = timezone.now()
    end_date = timezone.now() + timedelta(days=1)
    start_interview_date = timezone.now()
    end_interview_date = timezone.now() + timedelta(days=3)


class ApplicationProblemFactory(factory.DjangoModelFactory):
    class Meta:
        model = application_models.ApplicationProblem

    name = factory.LazyAttribute(lambda _: faker.text(max_nb_chars=255))
    description_url = factory.LazyAttribute(lambda _: faker.url())


class ApplicationFactory(factory.DjangoModelFactory):
    class Meta:
        model = application_models.Application

    application_info = factory.SubFactory(ApplicationInfoFactory)
    user = factory.SubFactory(BaseUserFactory)

    phone = faker.text(max_nb_chars=255)
    skype = faker.text(max_nb_chars=255)
    works_at = faker.text(max_nb_chars=255)
    studies_at = faker.text(max_nb_chars=255)


class ApplicationProblemSolutionFactory(factory.DjangoModelFactory):
    class Meta:
        model = application_models.ApplicationProblemSolution

    application = factory.SubFactory(ApplicationFactory)
    problem = factory.SubFactory(ApplicationProblemFactory)
    solution_url = faker.url()


class InterviewerFactory(BaseUserFactory):
    class Meta:
        model = interview_models.Interviewer


class InterviewerFreeTimeFactory(factory.DjangoModelFactory):
    class Meta:
        model = interview_models.InterviewerFreeTime

    interviewer = factory.SubFactory(InterviewerFactory)
    date = faker.date_time()
    start_time = timezone.now()
    end_time = timezone.now() + timedelta(minutes=270)
    buffer_time = faker.boolean()


class InterviewFactory(factory.DjangoModelFactory):
    class Meta:
        model = interview_models.Interview

    interviewer = factory.SubFactory(InterviewerFactory)
    application = factory.SubFactory(ApplicationFactory)
    date = faker.date_time()
    start_time = timezone.now()
    end_time = timezone.now() + timedelta(minutes=30)
    interviewer_time_slot = factory.SubFactory(InterviewerFreeTimeFactory)
    buffer_time = faker.boolean()
    # uuid = factory.LazyAttribute(lambda _: uuid.uuid4)

    interviewer_comment = faker.text()

    code_skills_rating = faker.random_number(digits=1)
    code_design_rating = faker.random_number(digits=1)
    fit_attitude_rating = faker.random_number(digits=1)

    has_confirmed = False
    has_received_email = False
    is_accepted = False
