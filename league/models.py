from django.db import models
from django.contrib.gis.db import models as gis_models
from django.core.exceptions import ValidationError

from teamplayer.models import Team, Player


class Fixture(models.Model):
    home_team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name='home_team', null=True)
    away_team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name='away_team', null=True)
    match_date = models.DateField(None)
    venue = models.CharField(max_length=100)
    location = gis_models.PointField(srid=4326, null=True, blank=True)
    kickoff = models.CharField(max_length=20)

    @property
    def lat_long(self):
        return list(getattr(self.location, 'coords', [])[::-1])

    def clean(self):
        if self.home_team == self.away_team:
            if self.home_team is None and self.away_team is None:
                pass
            else:
                raise ValidationError(
                    "Home team cannot be similar to the Away team.")


class FixtureResult(models.Model):
    fixture = models.ForeignKey(
        Fixture, on_delete=models.CASCADE, related_name='associated_fixture')
    home_team_result = models.PositiveIntegerField(default=0, blank=False)
    away_team_result = models.PositiveIntegerField(default=0, blank=False)
    MOTM = models.ForeignKey(
        Player, on_delete=models.SET_NULL, blank=True, null=True)

# class MatchdaySquad(models.Model):
#     pass
