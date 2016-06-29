from rest_framework import serializers
from education.serializers import (StudentSerializer, TeacherSerializer,
                                   CitySerializer)

from base_app.models import BaseUser, City
from hack_fmi.serializers import CompetitorSerializer


class BaseUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = BaseUser
        fields = (
            'email',
            'password',
            'first_name',
            'last_name',
            'studies_at',
            'works_at'
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class BaseUserMeSerializer(serializers.ModelSerializer):
    competitor = CompetitorSerializer(many=False, read_only=True)
    student = StudentSerializer(many=False, read_only=True)
    teacher = TeacherSerializer(many=False, read_only=True)
    birth_place = CitySerializer(read_only=True)

    class Meta:
        model = BaseUser
        fields = (
            'email',
            'first_name',
            'last_name',
            'avatar',
            'github_account',
            'linkedin_account',
            'twitter_account',
            'competitor',
            'student',
            'teacher',
            'works_at',
            'studies_at',
            'description',
            'birth_place',
        )


class UpdateBaseUserSerializer(serializers.ModelSerializer):
    birth_place = serializers.PrimaryKeyRelatedField(
        read_only=False,
        queryset=City.objects.all(),
    )
    birth_place_full = CitySerializer(read_only=True, source='birth_place')

    class Meta:
        model = BaseUser
        fields = (
            'first_name',
            'last_name',
            'avatar',
            'full_image',
            'github_account',
            'linkedin_account',
            'twitter_account',
            'works_at',
            'studies_at',
            'description',
            'birth_place',
            'birth_place_full',
        )
