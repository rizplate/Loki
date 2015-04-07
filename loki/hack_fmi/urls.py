from django.conf.urls import url

from djoser.views import ActivationView, LogoutView

from .views import (SkillListView, RegisterTeam, Login,
                    register_team, leave_team, me, RegistrationView, InvitationView)


urlpatterns = [
    url(r'^api/skills/$', SkillListView.as_view(), name='skills'),
    url(r'^api/register_team/$', register_team, name='register_team'),
    url(r'^api/teams/$', RegisterTeam.as_view(), name='teams'),

    url(r'^api/register/$', RegistrationView.as_view(), name='register'),
    url(r'^api/login/', Login.as_view(), name='login'),
    url(r'^api/logout/$', LogoutView.as_view(), name='activate'),
    url(r'^api/activate/$', ActivationView.as_view(), name='activate'),
    url(r'^api/me/$', me, name='me'),
    url(r'^api/leave_team/$', leave_team, name='leave_team'),
    url(r'^api/invitation/$', InvitationView.as_view(), name='invitation'),
]
