from django.db import models

# Create your models here.


class Match(models.Model):
    Match_id = models.CharField(primary_key=True, max_length=30, default='')
    Season = models.CharField(max_length=4, null=True, blank=True)
    Split = models.CharField(max_length=20, null=True, blank=True)
    Week = models.CharField(max_length=20, null=True, blank=True)
    Blue = models.CharField(max_length=5, null=True, blank=True)
    Red = models.CharField(max_length=5, null=True, blank=True)
    WinnerT = models.CharField(max_length=5, null=True, blank=True)
    Patch = models.CharField(max_length=50, null=True, blank=True)


class MatchHistory(models.Model):
    Match = models.ForeignKey(
        Match, on_delete=models.CASCADE, null=True, to_field='Match_id')
    Team = models.CharField(max_length=5, null=True, blank=True)
    Player = models.CharField(max_length=20, null=True, blank=True)
    Champion = models.CharField(max_length=20, null=True, blank=True)
    KDA = models.FloatField(null=True, blank=True)
    Gold = models.IntegerField(null=True, blank=True)
    TJK = models.IntegerField(null=True, blank=True)
    EJK = models.IntegerField(null=True, blank=True)
    JS = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"History for Match: {self.MatchId}"


class PicksBans(models.Model):
    Match = models.OneToOneField(
        Match, on_delete=models.CASCADE, null=True, to_field='Match_id')
    BB1 = models.CharField(max_length=50, null=True, blank=True)
    BB2 = models.CharField(max_length=50, null=True, blank=True)
    BB3 = models.CharField(max_length=50, null=True, blank=True)
    BB4 = models.CharField(max_length=50, null=True, blank=True)
    BB5 = models.CharField(max_length=50, null=True, blank=True)
    RB1 = models.CharField(max_length=50, null=True, blank=True)
    RB2 = models.CharField(max_length=50, null=True, blank=True)
    RB3 = models.CharField(max_length=50, null=True, blank=True)
    RB4 = models.CharField(max_length=50, null=True, blank=True)
    RB5 = models.CharField(max_length=50, null=True, blank=True)
    BPPlayer1 = models.CharField(max_length=50, null=True, blank=True)
    BP1 = models.CharField(max_length=50, null=True, blank=True)
    BPPlayer2 = models.CharField(max_length=50, null=True, blank=True)
    BP2 = models.CharField(max_length=50, null=True, blank=True)
    BPPlayer3 = models.CharField(max_length=50, null=True, blank=True)
    BP3 = models.CharField(max_length=50, null=True, blank=True)
    BPPlayer4 = models.CharField(max_length=50, null=True, blank=True)
    BP4 = models.CharField(max_length=50, null=True, blank=True)
    BPPlayer5 = models.CharField(max_length=50, null=True, blank=True)
    BP5 = models.CharField(max_length=50, null=True, blank=True)
    RPPlayer1 = models.CharField(max_length=50, null=True, blank=True)
    RP1 = models.CharField(max_length=50, null=True, blank=True)
    RPPlayer2 = models.CharField(max_length=50, null=True, blank=True)
    RP2 = models.CharField(max_length=50, null=True, blank=True)
    RPPlayer3 = models.CharField(max_length=50, null=True, blank=True)
    RP3 = models.CharField(max_length=50, null=True, blank=True)
    RPPlayer4 = models.CharField(max_length=50, null=True, blank=True)
    RP4 = models.CharField(max_length=50, null=True, blank=True)
    RPPlayer5 = models.CharField(max_length=50, null=True, blank=True)
    RP5 = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"Picks and Bans for Match: {self.MatchId}"


class MetaData(models.Model):
    Season = models.CharField(max_length=4, null=True, blank=True)
    Split = models.CharField(max_length=20, null=True, blank=True)
    Team = models.CharField(max_length=50, null=True, blank=True)
    Player = models.CharField(max_length=50, null=True, blank=True)
    Side = models.CharField(max_length=50, null=True, blank=True)
    Games = models.CharField(max_length=50, null=True, blank=True)
    Champion = models.CharField(max_length=50, null=True, blank=True)
    CKey = models.CharField(max_length=50, null=True, blank=True)
    Win = models.IntegerField(null=True, blank=True)
    Lose = models.IntegerField(null=True, blank=True)
    Kills = models.IntegerField(null=True, blank=True)
    Deaths = models.IntegerField(null=True, blank=True)
    Assists = models.IntegerField(null=True, blank=True)
    KillsC = models.IntegerField(null=True, blank=True)
    DeathsC = models.IntegerField(null=True, blank=True)
    AssistsC = models.IntegerField(null=True, blank=True)
    KDA = models.FloatField(null=True, blank=True)
    KDA_C = models.FloatField(null=True, blank=True)
    Bans = models.IntegerField(null=True, blank=True)
    Avg_BT = models.FloatField(null=True, blank=True)
    WR = models.FloatField(null=True, blank=True)
    Presence = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.Team} - {self.Player} - {self.Side} - {self.Split} vs {self.Champion}"


class Positions(models.Model):
    Season = models.CharField(max_length=4, null=True, blank=True)
    Split = models.CharField(max_length=20, null=True, blank=True)
    Week = models.CharField(max_length=20, null=True, blank=True)
    Type = models.CharField(max_length=10, null=True, blank=True)
    Team = models.CharField(max_length=5, null=True, blank=True)
    Player = models.CharField(max_length=50, null=True, blank=True)
    X = models.IntegerField(null=True, blank=True)
    Y = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Positions for Match: {self.MatchId}"
