import pandas as pd

from LOLStatium_app.models import *

class db():
    def createMatch(df):
        def matchId_Generator():
            if 'Week' in row['Week']:
                return row['Season']+row['Split'][0:2].upper()+'W'+row['Week'].split(' ')[1]+row['Blue']+row['Red']
            else:
                return row['Season']+row['Split'][0:2].upper()+'T'+row['Blue']+row['Red']
            
        for index, row in df.iterrows():
            match_instance = Match(
                Match_id=matchId_Generator(),
                Season=row['Season'],
                Split=row['Split'],
                Week=row['Week'],
                Blue=row['Blue'],
                Red=row['Red'],
                WinnerT=row['WinnerT'],
                Patch=row['Patch'],
            )
            match_instance.save()

    def insertMatchHistory(df: pd.DataFrame):

        def matchId_generator():
            if 'Week' in row['Week']:
                return row['Season']+row['Split'][0:2].upper()+'W'+row['Week'].split(' ')[1]+row['Blue']+row['Red']
            else:
                return row['Season']+row['Split'][0:2].upper()+'T'+row['Blue']+row['Red']


        # Itera sobre el dataframe y crea instancias del modelo con los datos
        for index, row in df.iterrows():
            matchHistory_instance = MatchHistory(
                Match=Match.objects.get(Match_id=matchId_generator()),
                Team=row['Team'],
                Player=row['Player'],
                Champion=row['Champion'],
                KDA=row['KDA'],
                Gold=row['Gold'],
                TJK=row['TeamJungle Kills'],
                EJK=row['EnemyJungle Kills'],
                JS=row['Jungle Share'],
            )
            matchHistory_instance.save()

    def insertPicksBans(df: pd.DataFrame):

        def matchId_Generator():
            if 'Week' in row['Week']:
                return row['Season']+row['Split'][0:2].upper()+'W'+row['Week'].split(' ')[1]+row['Blue']+row['Red']
            else:
                return row['Season']+row['Split'][0:2].upper()+'T'+row['Blue']+row['Red']
            
            

        # Itera sobre el dataframe y crea instancias del modelo con los datos
        for index, row in df.iterrows():
            picks_bans_instance = PicksBans(
                Match=Match.objects.create(
                    Match_id=matchId_Generator(),
                    Season=row['Season'],
                    Split=row['Split'],
                    Week=row['Week'],
                    Blue=row['Blue'],
                    Red=row['Red'],
                    WinnerT=row['WinnerT'],
                    Patch=row['Patch'],
                ),
                BB1=row['BB1'],
                BB2=row['BB2'],
                BB3=row['BB3'],
                BB4=row['BB4'],
                BB5=row['BB5'],
                RB1=row['RB1'],
                RB2=row['RB2'],
                RB3=row['RB3'],
                RB4=row['RB4'],
                RB5=row['RB5'],
                BPPlayer1=row['BPPlayer1'],
                BP1=row['BP1'],
                BPPlayer2=row['BPPlayer2'],
                BP2=row['BP2'],
                BPPlayer3=row['BPPlayer3'],
                BP3=row['BP3'],
                BPPlayer4=row['BPPlayer4'],
                BP4=row['BP4'],
                BPPlayer5=row['BPPlayer5'],
                BP5=row['BP5'],
                RPPlayer1=row['RPPlayer1'],
                RP1=row['RP1'],
                RPPlayer2=row['RPPlayer2'],
                RP2=row['RP2'],
                RPPlayer3=row['RPPlayer3'],
                RP3=row['RP3'],
                RPPlayer4=row['RPPlayer4'],
                RP4=row['RP4'],
                RPPlayer5=row['RPPlayer5'],
                RP5=row['RP5'],
            )
            picks_bans_instance.save()

    def insertMetaData(df: pd.DataFrame):
        # Itera sobre el dataframe y crea instancias del modelo con los datos
        for index, row in df.iterrows():
            metaData_instance = MetaData(
                Season=row['Season'],
                Team=row['team'],
                Player=row['Player'],
                Side=row['Side'],
                Split=row['Split'],
                Games=row['games'],
                Champion=row['Champion'],
                CKey=row['key'],
                Win=row['Win'],
                Lose=row['lose'],
                Kills=row['kills'],
                Deaths=row['deaths'],
                Assists=row['assists'],
                KillsC=row['killsC'],
                DeathsC=row['deathsC'],
                AssistsC=row['assistsC'],
                KDA=row['kda'],
                KDA_C=row['kdaC'],
                Bans=row['ban'],
                Avg_BT=row['Avg BT'],
                WR=row['wR'],
                Presence=row['Presence'],
            )
            metaData_instance.save()

    def insertPositions(df: pd.DataFrame):
        # Itera sobre el dataframe y crea instancias del modelo con los datos
        for index, row in df.iterrows():
            positions_instance = Positions(
                Season=row['Season'],
                Split=row['Split'],
                Week=row['Week'],
                Type=row['Type'],
                Team=row['Team'],
                Player=row['Player'],
                X=row['X'],
                Y=row['Y'],
            )
            positions_instance.save()
