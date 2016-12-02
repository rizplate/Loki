from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import TeamMembership, Season, SeasonCompetitorInfo, Competitor


@receiver(post_save, sender=TeamMembership)
def set_looking_for_team_to_false(sender, instance, created, **kwargs):
    if created:
        """
        We have unique_together = ('competitor', 'season')
        so the query will return one object or None.
        """
        season_competitor_info = instance.competitor.seasoncompetitorinfo_set.first()
        if season_competitor_info:
            season_competitor_info.looking_for_team = False
            season_competitor_info.save()


@receiver(post_save, sender=Season)
def create_season_competitor_infos_for_new_active_season(sender, instance, **kwargs):
    """
    When new active season is added, we'd want to create season
    competitor infos for all competitors for the new season.
    """
    if instance.is_active:
        if not SeasonCompetitorInfo.objects.filter(season=instance).exists():
            all_competitors = Competitor.objects.all()
            season_competitor_infos = []

            for competitor in all_competitors:
                season_competitor_infos.append(SeasonCompetitorInfo(competitor=competitor,
                                                                    season=instance))

            SeasonCompetitorInfo.objects.bulk_create(season_competitor_infos)
