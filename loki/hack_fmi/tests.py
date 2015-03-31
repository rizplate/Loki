from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Skill, Competitor, BaseUser, TeamMembership, Season, Team
from django.core import mail


class RegistrationTests(APITestCase):
    def setUp(self):
        self.skills = Skill.objects.create(name="C#")

    def test_register_user(self):
        data = {
            'email': 'ivo@abv.bg',
            'first_name': 'Ivo',
            'last_name': 'Bachvarov',
            'faculty_number': '123',
            'known_skills': '1',
            'password': '123'
        }
        url = reverse('hack_fmi:register')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Competitor.objects.count(), 1)
        self.assertEqual(BaseUser.objects.count(), 1)

    def test_registraion_full_name(self):
        data = {
            'email': 'ivo@abv.bg',
            'first_name': 'Ivo',
            'last_name': 'Bachvarov',
            'faculty_number': '123',
            'known_skills': '1',
            'password': '123'
        }
        url = reverse('hack_fmi:register')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_user_no_password(self):
        data = {
            'email': 'ivo@abv.bg',
            'first_name': 'Ivo',
            'last_name': 'Bachvarov',
            'faculty_number': '123',
            'known_skills': '1',
        }
        url = reverse('hack_fmi:register')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_email_sent(self):
        data = {
            'email': 'ivo@abv.bg',
            'first_name': 'Ivo',
            'last_name': ' Bachvarov',
            'faculty_number': '123',
            'known_skills': '1',
            'password': '123'
        }
        url = reverse('hack_fmi:register')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(mail.outbox), 1)

    def test_email_sent_new_tempalte(self):
        data = {
            'email': 'ivo@abv.bg',
            'first_name': 'Ivo',
            'last_name': ' Bachvarov',
            'faculty_number': '123',
            'known_skills': '1',
            'password': '123'
        }
        url = reverse('hack_fmi:register')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("Ти успешно се регистрира за HackFMI 5! През нашата нова система можеш лесно да намериш отбор, с който да се състезаваш.  Ако вече имаш идея можеш да създадеш отбор и да поканиш още хора в него.", mail.outbox[0].body)


class LoginTests(APITestCase):
    def setUp(self):
        self.skills = Skill.objects.create(name="C#")
        self.competitor = Competitor.objects.create(
            email='ivo@abv.bg',
            full_name='Ivo Naidobriq',
            faculty_number='123',
        )
        self.competitor.set_password('123')
        self.competitor.is_active = True
        self.competitor.save()

    def test_login(self):
        data = {
            'email': 'ivo@abv.bg',
            'password': '123',
        }
        url = reverse('hack_fmi:login')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_wrong_password(self):
        data = {
            'email': 'ivo@abv.bg',
            'password': '123321',
        }
        url = reverse('hack_fmi:login')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_wrong_not_competetor(self):
        self.baseuser = BaseUser.objects.create(
            email='baseuser@abv.bg',
            full_name='Ivo Naidobriq',
        )
        self.baseuser.set_password('123')
        self.baseuser.save()

        data = {
            'email': 'baseuser@abv.bg',
            'password': '123',
        }
        url = reverse('hack_fmi:login')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_data_after_login(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.competitor)
        url = reverse('hack_fmi:me')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.competitor.email)

    def test_get_data_not_login(self):
        url = reverse('hack_fmi:me')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TeamRegistrationTests(APITestCase):
    def setUp(self):
        self.skills = Skill.objects.create(name="C#")
        self.seasson = Season.objects.create(number=1, is_active=True)
        self.competitor = Competitor.objects.create(
            email='ivo@abv.bg',
            full_name='Ivo Naidobriq',
            faculty_number='123',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.competitor)

    def test_register_team(self):
        data = {
            'name': 'Pandas',
            'idea_description': 'GameDevelopers',
            'repository': 'https://github.com/HackSoftware',
            'technologies': 1,
        }
        url = reverse('hack_fmi:register_team')
        response = self.client.post(url, data, format='json')

        self.assertEqual(len(response.data['members']), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # print(response.data)
        # self.assertEqual(len(response.data['technologies']), 1)

    def test_registered_team_has_leader(self):
        data = {
            'name': 'Pandas',
            'idea_description': 'GameDevelopers',
            'repository': 'https://github.com/HackSoftware',
            'technologies': 1,
        }
        url = reverse('hack_fmi:register_team')
        self.client.post(url, data, format='json')
        team_membership = TeamMembership.objects.get(id=1)
        self.assertEqual(self.competitor, team_membership.competitor)
        self.assertTrue(team_membership.is_leader)
        url = reverse('hack_fmi:me')

    def test_register_more_than_one_team(self):
        data = {
           'name': 'Pandas',
           'idea_description': 'GameDevelopers',
           'repository': 'https://github.com/HackSoftware',
           'technologies': 1,
           }
        url = reverse('hack_fmi:register_team')
        first_response = self.client.post(url, data, format='json')

        data = {
           'name': 'Pandass',
           'idea_description': 'GameDeveloperss',
           'repository': 'https://github.com/HackSoftwares',
           'technologies': 1,
           }
        url = reverse('hack_fmi:register_team')
        second_response = self.client.post(url, data, format='json')
        self.assertEqual(first_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(second_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Team.objects.count(), 1)

    def test_list_team_by_id(self):
        Team.objects.create(
            name='Pandass',
            idea_description='GameDevelopers',
            repository='https://github.com/HackSoftware',
            season=self.seasson
        )
        Team.objects.create(
            name='Pandass2',
            idea_description='GameDevelopers',
            repository='https://github.com/HackSoftware',
            season=self.seasson
        )
        url_get = reverse('hack_fmi:teams')
        data = {'id': 2}
        response = self.client.get(url_get, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Pandass2')

    def test_list_team_all(self):
        Team.objects.create(
            name='Pandass',
            idea_description='GameDevelopers',
            repository='https://github.com/HackSoftware',
            season=self.seasson
        )
        Team.objects.create(
            name='Pandass2',
            idea_description='GameDevelopers',
            repository='https://github.com/HackSoftware',
            season=self.seasson
        )

        url_get = reverse('hack_fmi:teams')

        response = self.client.get(url_get, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

