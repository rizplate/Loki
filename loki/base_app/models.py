from django.utils import timezone
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,
                                        BaseUserManager, PermissionsMixin)
from ckeditor.fields import RichTextField

from loki.settings import MEDIA_ROOT
from image_cropping.fields import ImageRatioField, ImageCropField

class Company(models.Model):
    name = models.CharField(max_length=100, unique=True)
    logo_url = models.URLField(blank=True)
    logo = models.ImageField(upload_to="partners_logoes", null=True, blank=True)
    jobs_link = models.URLField(blank=True)

    def get_logo(self):
        if self.logo:
            return MEDIA_ROOT + 'logos/' + str(self.pk) + '.JPG'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Companies'


class Partner(models.Model):
    company = models.OneToOneField(Company, primary_key=True)
    description = RichTextField(blank=False)
    facebook = models.URLField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    money_spent = models.PositiveIntegerField(default=0, blank=False, null=False)
    ordering = models.PositiveSmallIntegerField(default=0, blank=False, null=False)

    twitter = models.URLField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)

    video_presentation = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ('ordering',)

    def __str__(self):
        return self.company.name


class GeneralPartner(models.Model):
    partner = models.OneToOneField(Partner, primary_key=True)

    def __str__(self):
        return self.partner.company.name


class HostingPartner(models.Model):
    partner = models.OneToOneField(Partner, primary_key=True)

    def __str__(self):
        return self.partner.company.name


class City(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Cities'


class EducationPlace(models.Model):
    name = models.CharField(max_length=1000)
    city = models.ForeignKey(City)

    def is_uni(self):
        return hasattr(self, 'university')

    def is_school(self):
        return hasattr(self, 'school')

    def is_academy(self):
        return hasattr(self, 'academy')

    def __str__(self):
        return "{} ({})".format(self.name, self.city)

    class Meta:
        unique_together = (('name', 'city'),)


class University(EducationPlace):
    class Meta:
        verbose_name_plural = 'Universities'


class Faculty(models.Model):
    university = models.ForeignKey(University)
    name = models.CharField(max_length=1000)
    abbreviation = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (('university', 'name'),)
        verbose_name_plural = 'Faculties'


class Subject(models.Model):
    faculty = models.ForeignKey(Faculty)
    name = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

    def represent(self):
        return " / ".join([self.name, self.faculty.name, self.faculty.uni.name, self.faculty.uni.city.name])

    class Meta:
        unique_together = (('faculty', 'name'),)


class School(EducationPlace):
    pass


class Academy(EducationPlace):
    class Meta:
        verbose_name_plural = 'Academies'


class UserManager(BaseUserManager):

    def __create_user(self, email, password, full_name,
                      is_staff=False, is_active=False, is_superuser=False, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff,
                          is_active=is_active,
                          full_name=full_name,
                          is_superuser=is_superuser,
                          **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, full_name='', **kwargs):
        return self.__create_user(email, password, full_name, is_staff=False, is_active=False,
                                  is_superuser=False, **kwargs)

    def create_superuser(self, email, password, full_name=''):
        return self.__create_user(email, password, full_name, is_staff=True,
                                  is_active=True, is_superuser=True)

    def create(self, **kwargs):
        return self.create_user(**kwargs)


class BaseUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    birth_place = models.ForeignKey(City, null=True, blank=True)

    github_account = models.URLField(null=True, blank=True)
    linkedin_account = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    twitter_account = models.URLField(null=True, blank=True)

    works_at = models.CharField(null=True, blank=True, max_length=110)
    studies_at = models.CharField(blank=True, null=True, max_length=110)

    avatar = ImageCropField(blank=True, null=True)
    full_image = ImageCropField(upload_to='avatars/', blank=True, null=True)
    cropping = ImageRatioField('full_image', '300x300')

    education_info = models.ManyToManyField(EducationPlace, through='EducationInfo', related_name='info')

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def get_competitor(self):
        try:
            return self.competitor
        except:
            return False

    def get_student(self):
        try:
            return self.student
        except:
            return False

    def get_teacher(self):
        try:
            return self.teacher
        except:
            return False

    # def make_competitor(self):
    #     competitor = Competitor(baseuser_ptr_id=self.id)
    #     competitor.save()
    #     competitor.__dict__.update(self.__dict__)

    #     return competitor.save()


class EducationInfo(models.Model):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    place = models.ForeignKey(EducationPlace, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField()

    faculty = models.ForeignKey(Faculty, blank=True, null=True, related_name="related_fac_to_user")
    subject = models.ForeignKey(Subject, blank=True, null=True, related_name="related_subj_to_user")

    def save(self, *args, **kwargs):
        '''On save, update created_at and updated_at timestamps
           Idea based on http://stackoverflow.com/questions/1737017/django-auto-now-and-auto-now-add/1737078#1737078
        '''

        if not self.id:
            self.created_at = timezone.now()

        self.updated_at = timezone.now()

        return super().save(*args, **kwargs)


class BaseUserRegisterToken(models.Model):
    user = models.OneToOneField(BaseUser)
    token = models.CharField(unique=True, max_length=100)


class BaseUserPasswordResetToken(models.Model):
    user = models.OneToOneField(BaseUser)
    token = models.CharField(unique=True, max_length=100)


class RegisterOrigin(models.Model):
    """
    This is a model that describes all of the systems that are integrated
    with Loki's user management. (HackFMI, Education)
    This is used on user activation. Users are being redirect to 'redirect_url'
    after getting 'name' from a GET parameter.
    """
    name = models.SlugField()
    redirect_url = models.URLField()
