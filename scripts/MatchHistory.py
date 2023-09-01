import pandas as pd
from Web_scrap import Scraping
from Web_scrap import *
from tqdm import tqdm


def matchHistory(json_data: dict, blueTeam: str,redTeam: str, split: str, week: str, V4: bool = False) -> pd.DataFrame:
    """
    La función toma datos JSON, equipos, división, semana y un valor booleano y devuelve un Pandas
    DataFrame con datos del historial de partidos para cada jugador.

    Args:
      json_data (dict): un diccionario que contiene los datos de la coincidencia en formato JSON
      teams (str): una cadena que representa a los dos equipos que jugaron el partido
      split (str): El split de la liga o torneo al que pertenece el partido (por ejemplo, Spring Split,
    Summer Split).
      week (str): El parámetro semana es una cadena que representa el número de semana del historial de
    partidos.
      V4 (bool): Un parámetro booleano que indica si los datos están en formato V4 o no. Defaults to
    False

    Returns:
      La función `matchHistory` devuelve un Pandas DataFrame que contiene datos del historial de
    partidos para un juego, división y semana determinados de League of Legends, así como los equipos
    involucrados en el juego. La función toma un objeto JSON que contiene los datos de la coincidencia,
    así como argumentos opcionales sobre si los datos están en formato V4 y si se incluyen datos de la
    jungla.
    """
    # Normalizo el json para tratar los datos por jugador
    df = pd.json_normalize(json_data, 'participants')
    # Inicializo el dataFrame del Match History
    df_MH = pd.DataFrame()
    try:
        if V4:
            # Extraigo los datos que quiero dentro del df normalizado
            df = df[['participantId', 'championId', 'stats.kills', 'stats.deaths', 'stats.assists',
                     'stats.goldEarned', 'stats.neutralMinionsKilledTeamJungle', 'stats.neutralMinionsKilledEnemyJungle']]

            players = []
            champions = []
            for participant in df['participantId']:
                players.append(Scraping.getParticipantByIdV4(
                    json_data, participant))
            for champ in df['championId']:
                champions.append(Scraping.getChampionById(champ))

            df_players = pd.DataFrame(players)
            df_MH['Team'] = df_players[0].str.split(' ').str[0]
            df_MH['Player'] = df_players[0].str.split(' ').str[1]
            df_MH['Champion'] = pd.DataFrame(champions)
            df_MH['KDA'] = df[['stats.kills', 'stats.assists']].sum(
                axis=1).divide(df['stats.deaths']).round(2)
            df_MH['Gold'] = df['stats.goldEarned']
            df_MH['TeamJungle Kills'] = df['stats.neutralMinionsKilledTeamJungle']
            df_MH['EnemyJungle Kills'] = df['stats.neutralMinionsKilledEnemyJungle']
            df_MH['Jungle Share'] = df_MH[[
                'TeamJungle Kills', 'EnemyJungle Kills']].sum(axis=1)

        elif V4 == False:
            # Ya que el nombre del jugador se compone por equipo y jugador, lo divido en dos columnas
            df_MH['Team'] = df['summonerName'].str.split(' ').str[0]
            df_MH['Player'] = df['summonerName'].str.split(' ').str[1]

            # Extraigo los datos que quiero dentro del df normalizado
            df_MH = pd.concat([df_MH, df[['championName', 'challenges.kda',
                                          'goldEarned', 'challenges.teamDamagePercentage']]], axis=1).round(2)

            # Se obtiene el Gold / Damage, que es el calculo del oro obtenido entre el porcentaje de daño de equipo
            df_MH["Gold/Damage"] = df['goldEarned'].multiply(
                df['challenges.teamDamagePercentage']).round(2)

            # Se obtiene el Jugle Share, que es la suma de las kills de la jungla en ambos lados
            df_cs = df[['challenges.alliedJungleMonsterKills',
                        'challenges.enemyJungleMonsterKills']].astype(int)
            df_cs['Jungle Share'] = df_cs.sum(axis=1)

            # Se le añade jungle share al df final
            df_MH = pd.concat([df_MH, df_cs], axis=1)
            # Se cambia el nombre de las columnas
            df_MH = df_MH.rename(columns={'championName': 'Champion', 'challenges.kda': 'KDA', 'goldEarned': 'Gold',
                                          'challenges.teamDamagePercentage': 'TDamage', 'challenges.alliedJungleMonsterKills': 'TeamJungle Kills',
                                          'challenges.enemyJungleMonsterKills': 'EnemyJungle Kills'})

        # Se inserta el Split, la semana y el juego a la que pertenece el partido
        df_MH.insert(0, 'Split', split)
        df_MH.insert(1, 'Week', week)
        df_MH.insert(2, 'Blue', blueTeam)
        df_MH.insert(3, 'Red', redTeam)

        return df_MH

    except KeyError:
        return pd.DataFrame()


def getDF_MH(league: str, season: str, download: bool = False) -> pd.DataFrame:
    """
    Esta función extrae los datos del historial de partidos de una liga y una temporada determinadas, y
    los devuelve como un marco de datos de pandas, con la opción de descargarlo como un archivo CSV.

    Args:
      league (str): una cadena que representa el nombre de la liga para la que queremos obtener los
    datos del historial de partidos.
      season (str): El parámetro de temporada es una cadena que representa el año o rango de años para
    los que el usuario desea obtener los datos del historial de partidos. Por ejemplo, "2021" o
    "2019-2020".
      download (bool): Un parámetro booleano que indica si descargar el DataFrame resultante como un
    archivo CSV o no. Si se establece en True, la función guardará el DataFrame como un archivo CSV en
    la carpeta "Descargar" con el nombre "Picks&Bans-{liga}_{temporada}.csv". Si se establece en Falso,
    el. Defaults to False

    Returns:
      un marco de datos de pandas que contiene datos del historial de partidos para una liga y una
    temporada determinadas. Si el parámetro de descarga se establece en Verdadero, la función también
    guardará los datos como un archivo CSV en una carpeta "Descargar". Si no hay datos disponibles para
    la liga y la temporada dadas, la función imprimirá "No hay datos" y devolverá Ninguno.
    """
    # Se inicializa el df final
    df_final = pd.DataFrame()
    # Se obtienen los datos de la Liga en cierta temporada
    data = Scraping.games(league.upper(), season)

    if league in leagues and data[0]:  # Si hay datos
      # Se guardan en listas
        split = data[0]
        week = data[1]
        BlueTeams = data[2]
        RedTeams = data[3]
        links = data[4]

        # Se recorren las listas para meter los datos en el DF final
        for i in tqdm(range(0, len(links)), unit='MB', desc=f"Match History {league} {season}", colour="Cyan", leave=False):
            if 'V4' in links[i]:
                V4 = True
            else:
                V4 = False

            df_match = matchHistory(Scraping.getJson(
                links[i]), BlueTeams[i],RedTeams[i], split[i], week[i], V4)

            if not df_match.empty:
                df_final = pd.concat([df_final, df_match], ignore_index=True)

        df_final.insert(0, 'Season', season)

        if download:  # Se crea el csv
            df_final.to_csv(
                f'Model\\Download\\MatchHistory-{league.upper()}_{season}.csv', index=False)
            print(
                'Datos guardados en: Model\\Download\\MatchHistory-{}_{}.csv'.format(league.upper(), season))

    return df_final


if __name__ == "__main__":
    print(getDF_MH('LEC', '2020')['TDamage'])
