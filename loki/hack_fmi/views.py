from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework_jwt.views import ObtainJSONWebToken

from .models import Skill, Competitor, Team, TeamMembership
from .serializers import SkillSerializer, CompetitorSerializer, TeamSerializer

from django.core.mail import send_mail


class SkillListView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        languages = Skill.objects.all()
        serializer = SkillSerializer(languages, many=True)
        return Response(serializer.data)


class CompetitorListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        competitors = Competitor.objects.all()
        serializer = CompetitorSerializer(competitors, many=True)
        return Response(serializer.data)


class TeamListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes((AllowAny,))
def register(request):
    serializer = CompetitorSerializer(data=request.data)
    if serializer.is_valid():
        new_user = serializer.save()
        new_user.set_password(serializer._validated_data['password'])
        send_mail('HAckFMI регистрация', 'Here is the message.', 'from@example.com', (new_user.email,), fail_silently=False)
        new_user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Login(ObtainJSONWebToken):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.object.get('user')
            if not user.get_competitor():
                return Response('Not a HackFMI user.', status=status.HTTP_403_FORBIDDEN)
        return super(Login, self).post(request)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def register_team(request):
    logged_user = request.user
    serializer = TeamSerializer(data=request.data)
    if not logged_user.get_competitor():
        return Response('Not a HackFMI user.', status=status.HTTP_403_FORBIDDEN)

    if serializer.is_valid():
        team = serializer.save()
        team_membership = TeamMembership.objects.create(
            competitor=logged_user.competitor,
            team=team,
            is_leader=True
        )
        team_membership.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def me(request):
    logged_competitor = request.user.get_competitor()
    serializer = CompetitorSerializer(logged_competitor, many=False)

    return Response(serializer.data, status=status.HTTP_200_OK)
