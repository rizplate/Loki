from django.core.management.base import BaseCommand, CommandError
from hack_fmi.models import Room, Team, Season


class Command(BaseCommand):
    help = 'distributes the teams in rooms'

    def handle(self, *args, **options):
        latest_season = Season.objects.get(is_active=True)
        all_rooms = Room.objects.filter(season=latest_season)

        capacity = sum([room.capacity for room in all_rooms])
        all_teams = Team.objects.filter(season=latest_season)

        if len(all_teams) > capacity:
            error = "We have {} capacity and {} teams.".format(capacity, len(all_teams))
            raise CommandError(error)

        all_teams = list(all_teams)
        while all_teams:
            for room in all_rooms:
                if not room.is_full():
                    current_team = all_teams.pop()
                    current_team.room = room
                    current_team.save()
