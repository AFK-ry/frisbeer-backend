from rest_framework import serializers, viewsets
from rest_framework.exceptions import ValidationError

from frisbeer.models import *


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'name', 'elo')
        read_only_fields = ('elo',)


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class PlayersValidator:
    def __call__(self, values):
        players = values.get("players", None)
        if not players or len(players) != 6:
            raise ValidationError("Round requires exactly six players")


class RoundPlayerValidator:
    def __call__(self, values):
        team1 = set(values["team1"])
        team2 = set(values["team2"])
        if len(team1) != 3 or len(team2) != 3:
            raise ValidationError("Teams must consist of exactly three players")

        if team1.intersection(team2):
            raise ValidationError("Teams can't contain same players")


class RoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Round
        fields = ('id', 'winner', 'date', 'team1', "team2",)
        validators = [
            RoundPlayerValidator()
        ]

    def create(self, validated_data):
        round = super().create(validated_data)
        return round


class RoundViewSet(viewsets.ModelViewSet):
    queryset = Round.objects.all()
    serializer_class = RoundSerializer

from frisbeer import signals
