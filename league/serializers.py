import re

from rest_framework import serializers
# from django.utils.translation import ugettext_lazy as _


from .models import *


class FixtureSerializer(serializers.ModelSerializer):
    home_team = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Team.objects.all(),
    )
    away_team = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Team.objects.all(),
    )

    class Meta:
        model = Fixture
        fields = '__all__'


class ListFixtureSerializer(serializers.ModelSerializer):
    home_team = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Team.objects.all(),
    )
    away_team = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Team.objects.all(),
    )

    class Meta:
        model = Fixture
        fields = ['id', 'home_team', 'away_team', 'match_date', 'venue']


class CreateFixtureSerializer(serializers.ModelSerializer):
    home_team = serializers.CharField()
    away_team = serializers.CharField()
    match_date = serializers.DateField()
    venue = serializers.CharField()
    kickoff = serializers.CharField()

    class Meta:
        model = Fixture
        fields = ['home_team', 'away_team', 'match_date', 'venue', 'kickoff']
        validators: list = []

    def validate_home_team(self, value):
        try:
            team = Team.objects.get(name=value)
            value = team
        except Exception:
            raise serializers.ValidationError("Please enter a valid team")
        return value

    def validate_away_team(self, value):
        try:
            team = Team.objects.get(name=value)
            value = team
        except Exception:
            raise serializers.ValidationError("Please enter a valid team")
        return value

    def validate_match_date(self, value):
        return value

    def validate_venue(self, value):
        return value

    def validate_kickoff(self, value):
        return value

    def validate(self, attrs):
        instance = Fixture(**attrs)
        instance.clean()
        return attrs

    def create(self, validated_data):
        try:
            fixture = Fixture.objects.create(
                home_team=validated_data['home_team'],
                away_team=validated_data['away_team'],
                match_date=validated_data['match_date'],
                venue=validated_data['venue'],
                kickoff=validated_data['kickoff'],
            )
            fixture.save()

            validated_data["fixture"] = fixture

        except Exception:
            raise serializers.ValidationError("Fixture creation failed.")

        return validated_data


class UpdateFixtureSerializer(serializers.Serializer):
    home_team = serializers.CharField()
    away_team = serializers.CharField()
    match_date = serializers.DateField()
    venue = serializers.CharField()
    kickoff = serializers.CharField()

    class Meta:
        model = Fixture
        fields = ['home_team', 'away_team', 'match_date', 'venue', 'kickoff']
        validators: list = []

    def validate_home_team(self, value):
        try:
            team = Team.objects.get(name=value)
            value = team
        except Exception:
            raise serializers.ValidationError("Please enter a valid team")
        return value

    def validate_away_team(self, value):
        try:
            team = Team.objects.get(name=value)
            value = team
        except Exception:
            raise serializers.ValidationError("Please enter a valid team")
        return value

    def validate_match_date(self, value):
        return value

    def validate_venue(self, value):
        return value

    def validate_kickoff(self, value):
        return value

    def validate(self, attrs):
        instance = Fixture(**attrs)
        instance.clean()
        return attrs

    def save(self, *args, **kwargs):
        if self.partial:
            if self.validated_data:
                if self.validated_data.get("home_team"):
                    self.instance.home_team = self.validated_data.get(
                        "home_team")
                if self.validated_data.get("away_team"):
                    self.instance.away_team = self.validated_data.get(
                        "away_team")
                if self.validated_data.get("match_date"):
                    self.instance.match_date = self.validated_data.get(
                        "match_date")
                if self.validated_data.get("venue"):
                    self.instance.venue = self.validated_data.get(
                        "venue")
                if self.validated_data.get("kickoff"):
                    self.instance.kickoff = self.validated_data.get(
                        "kickoff")
                self.instance.save()
            else:
                return "No data to update"
        else:
            self.instance.home_team = self.validated_data.get("home_team")
            self.instance.away_team = self.validated_data.get("away_team")
            self.instance.match_date = self.validated_data.get("match_date")
            self.instance.venue = self.validated_data.get("venue")
            self.instance.kickoff = self.validated_data.get("kickoff")
            self.instance.save()


class FixtureResultSerializer(serializers.ModelSerializer):
    home_team_result = serializers.IntegerField()
    away_team_result = serializers.IntegerField()
    fixture = serializers.SerializerMethodField()
    MOTM = serializers.SerializerMethodField()

    class Meta:
        model = FixtureResult
        fields = '__all__'

    def get_fixture(self, obj) -> str:
        return f'{obj.fixture.id}. {obj.fixture.home_team} VS {obj.fixture.away_team}'

    def get_MOTM(self, obj) -> str:
        return obj.MOTM.user.username


class ListFixtureResultSerializer(serializers.ModelSerializer):
    home_team_result = serializers.IntegerField()
    away_team_result = serializers.IntegerField()
    fixture = serializers.SerializerMethodField()
    MOTM = serializers.SerializerMethodField()

    class Meta:
        model = FixtureResult
        fields = ['fixture', 'home_team_result', 'away_team_result', 'MOTM']

    def get_fixture(self, obj) -> str:
        return f'{obj.fixture.id}. {obj.fixture.home_team} VS {obj.fixture.away_team}'

    def get_MOTM(self, obj) -> str:
        return obj.MOTM.user.username


class CreateFixtureResultSerializer(serializers.ModelSerializer):
    fixture = serializers.CharField()
    home_team_result = serializers.IntegerField()
    away_team_result = serializers.IntegerField()
    MOTM = serializers.CharField()

    class Meta:
        model = FixtureResult
        fields = ['fixture', 'home_team_result', 'away_team_result', 'MOTM']
        validators: list = []

    def validate_fixture(self, value):
        fixture = Fixture.objects.get(id=value)
        fixture_results = fixture.associated_fixture.all().count()

        if fixture_results:
            raise serializers.ValidationError(
                "A fixture cannot have more than one result.")
        value = fixture
        return value

    def validate_home_team_result(self, value):
        return value

    def validate_away_team_result(self, value):
        return value

    def validate_MOTM(self, value):
        player = Player.objects.get(id=value)
        value = player
        return value

    def create(self, validated_data):
        try:
            fixture_result = FixtureResult.objects.create(
                fixture=validated_data['fixture'],
                home_team_result=validated_data['home_team_result'],
                away_team_result=validated_data['away_team_result'],
                MOTM=validated_data['MOTM']
            )
            fixture_result.save()

            validated_data["fixture_result"] = fixture_result

        except Exception:
            raise serializers.ValidationError(
                "Fixture-result creation failed.")

        return validated_data


class UpdateFixtureResultSerializer(serializers.Serializer):
    fixture = serializers.CharField()
    home_team_result = serializers.IntegerField()
    away_team_result = serializers.IntegerField()
    MOTM = serializers.CharField()

    class Meta:
        model = FixtureResult
        fields = ['fixture', 'home_team_result', 'away_team_result', 'MOTM']
        validators: list = []

    def validate_fixture(self, value):
        fixture = Fixture.objects.get(id=value)

        if not self.instance.fixture == fixture:
            raise serializers.ValidationError("The fixture must be the same.")
        value = fixture
        return value

    def validate_home_team_result(self, value):
        return value

    def validate_away_team_result(self, value):
        return value

    def validate_MOTM(self, value):
        player = Player.objects.get(id=value)
        value = player
        return value

    def save(self, *args, **kwargs):
        if self.partial:
            if self.validated_data:
                if self.validated_data.get("fixture"):
                    self.instance.fixture = self.validated_data.get("fixture")
                if self.validated_data.get("home_team_result"):
                    self.instance.home_team_result = self.validated_data.get(
                        "home_team_result")
                if self.validated_data.get("away_team_result"):
                    self.instance.away_team_result = self.validated_data.get(
                        "away_team_result")
                if self.validated_data.get("MOTM"):
                    self.instance.MOTM = self.validated_data.get(
                        "MOTM")
                self.instance.save()
            else:
                return "No data to update"
        else:
            self.instance.fixture = self.validated_data.get("fixture")
            self.instance.home_team_result = self.validated_data.get(
                "home_team_result")
            self.instance.away_team_result = self.validated_data.get(
                "away_team_result")
            self.instance.MOTM = self.validated_data.get("MOTM")
            self.instance.save()
