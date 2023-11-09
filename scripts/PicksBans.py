import pandas as pd
from Web_scrap import Scraping
from Web_scrap import splits
from tqdm import tqdm


def getPatch(json_data: dict):
    """Método para obtener el parche del juego

    Args:
        json_data (json): Json con los datos del juego

    Returns:
        str: Parche del juego
    """
    out = str(json_data['gameVersion']).split('.')
    return out[0]+"."+out[1]


def formatDF(df: pd.DataFrame, side: str, type: str):
    """Método para formatear el DataFrame de los picks y bans.
    Dependen de si son Picks, Bans o Blue, Red.

    Args:
        df (df): DataFrame a formatear
        side (str): Red/blue
        type (str): Pick/ban

    Returns:
        df: DataFrame formateado
    """
    if (side == 'blue'):  # Si es del lado azul
        col_name = 'B'  # creo una variable para el nombre de la columna y le pongo una B inicial

    elif (side == 'red'):  # Si es rojo
        col_name = 'R'  # le coloco una R inicial

    if (type == 'ban'):  # Si es para formatear un ban
        col_name = col_name+"B"  # Se le añade una B para identificar que es un Ban
        # Transpongo y formateo el dataFrame de salida con los bans
        return df.transpose().rename(columns={0: col_name+'1', 1: col_name+'2',
                                              2: col_name+'3', 3: col_name+'4',
                                              4: col_name+'5'})

    elif (type == 'pick'):  # Si es para formatear un pick
        col_name = col_name+"P"  # Se le añade una P para identificar que es un Pick
        # Creo otra variable para la columna de los jugadores
        col_player = col_name+"Player"
        # Transpongo y formateo el dataFrame de salida con los picks
        return df.transpose().rename(columns={0: col_player+'1', 1: col_name+'1',
                                              2: col_player+'2', 3: col_name+'2',
                                              4: col_player+'3', 5: col_name+'3',
                                              6: col_player+'4', 7: col_name+'4',
                                              8: col_player+'5', 9: col_name+'5'})


def picks(json_data: dict):
    """Método para obtener los picks de un json

    Args:
        json_data (json): json de entrada con los datos del juego

    Returns:
        df: DataFrame con los picks
    """
    participants = json_data['participants']  # Se obtiene el nodo de participantes del JSON

    # Se crean dos listas vacias para almacenar los picks tanto del equipo azul como el rojo.
    blue_picks = []
    red_picks = []

    for participant in participants:  # Se recorre e itera el nodo participantes
        try:
            # Se almacena el nombre del campeón
            champion_name = participant['championName']
            # Se almacena el nombre del jugador
            summoner_name = participant['summonerName'].split(' ')[1]

        # En algunos json, la disposición de los datos es distinta. Por eso salta KeyError
        except KeyError:
            # Obtengo el id del campeón y busco su nombre por ID
            championId = participant['championId']
            champion_name = Scraping.getChampionById(championId)

            # Obtengo el id del jugador
            participantId = participant['participantId']
            # Obtengo las identidades de los jugadores para hacer una busqueda del nombre del jugador
            summonerIds = json_data['participantIdentities']
            # Las recorro para obtener el nombre del jugador
            for summoner in summonerIds:
                if (summoner['participantId'] == participantId):
                    summoner_name = summoner['player']['summonerName'].split(' ')[
                        1]

        # Se agregan los datos obtenidos anteriormente a la lista correspondiente
        # Si su teamId es 100, es que pertenece al equipo azul
        if participant['teamId'] == 100:
            blue_picks.append(summoner_name)
            blue_picks.append(champion_name)
        else:  # Sino al rojo
            red_picks.append(summoner_name)
            red_picks.append(champion_name)

    # Creamos los dataFrames
    df_blue = pd.DataFrame(blue_picks)
    df_red = pd.DataFrame(red_picks)

    # Se transponen los DataFrames y se renombran las columnas
    df_blue = formatDF(df_blue, 'blue', 'pick')
    df_red = formatDF(df_red, 'red', 'pick')

    # Se devuelve el conjunto del Dataframe del equipo azul y del rojo
    return pd.concat([df_blue, df_red], axis=1)


def bans(json_data: dict):
    """Método para sacar un DataFrame con los picks.

    Args:
        json_data (json): json con la información de la partida
    """
    teams = json_data['teams']
  # Se crea dos listas vacías, una para cada equipo
    blue_bans = []
    red_bans = []

  # Iterar a través de la lista de equipos
    for team in teams:
        # Iterar a través de su lista de selecciones de campeones
        for ban in team['bans']:
            champion_name = Scraping.getChampionById(ban['championId'])
            # Para cada selección de campeón, agregarla a la lista correspondiente al equipo
            if team['teamId'] == 100:
                blue_bans.append(champion_name)
            else:
                red_bans.append(champion_name)

    df_blue = pd.DataFrame(blue_bans)
    df_red = pd.DataFrame(red_bans)

    df_blue = formatDF(df_blue, 'blue', 'ban')
    df_red = formatDF(df_red, 'red', 'ban')

    return pd.concat([df_blue, df_red], axis=1)

# Picks y bans


def picksBans(split: str, week: str, blueTeam: str, redTeam: str, json_data: dict) -> pd.DataFrame:
    """Método que genera un DataFrame de una sola partida

    Args:
        json_data (json): Json con los datos de la partida
        blueTeam (str): Equipo del lado azul
        redTeam (str): Equipo del lado rojo
        weeks (str): Semanas

    Returns:
        pd.DataFrame: DataFrame final con los picks y bans
    """
    teams = json_data['teams']
    # Se mira que equipo ha ganado y se
    if (teams[0]['win'] == True):
        winner = blueTeam
    else:
        winner = redTeam

    df_bans = bans(json_data)  # Obtención del DF de los bans
    df_picks = picks(json_data)  # Obtención del DF de los picks
    df_global = pd.concat([df_bans, df_picks], axis=1)  # Se concatenan los DF
    df_global.insert(0, 'Split', split)
    df_global.insert(1, 'Week', week)  # Se inserta la semana
    # Se insertan el equipo azul y rojo
    df_global.insert(2, 'Blue', blueTeam)
    df_global.insert(3, 'Red', redTeam)
    # Se inserta el equipo campeon
    df_global.insert(4, 'WinnerT', winner)
    # Se inserta el parche del juego
    df_global.insert(5, 'Patch', getPatch(json_data))

    return df_global


def getDF_picksBans(league: str, season: str, download: bool = False) -> pd.DataFrame:
    """Método que obtiene todos los enlaces de una temporada, de una región y un año
    en concreto y los transforma en un Dataframe.
    Finalmente genera un csv
    Args:
        league (str): región de la que se quieren obtener los datos
        season (str): año
        download (bool, optional): _description_. Defaults to False.
    Returns:
        pd.DataFrame: Dataframe final de una temporada        
    """
    # Se inicializa el df final
    df_final = pd.DataFrame()

    # Se buscan los datos
    data = Scraping.games(league.upper(), season)

    if data:  # Si hay datos
        # Se guardan en listas
        ssons = data[0]
        weeks = data[1]
        blueTeams = data[2]
        redTeams = data[3]
        links = data[4]

        # Se recorren las listas para meter los datos en el DF final
        for i in tqdm(range(len(links)), unit='MB', desc=f"Picks y bans {league} {season}", colour='Blue', leave=False):
            # Se concatenan los DataFrames
            df_final = pd.concat([df_final,
                                  picksBans(ssons[i], weeks[i], blueTeams[i],
                                            redTeams[i], Scraping.getJson(links[i]))], ignore_index=True)

        # Se añade una columna con la Split a la que pertenece
        df_final.insert(0, 'Season', season)

        # Se crea el csv
        if download:
            df_final.to_csv(
                'Model\\Download\\Picks&Bans-{}_{}.csv'.format(league.upper(), season), index=False)
            print(
                'Model\\Datos guardados en: Download\\Picks&Bans-{}_{}.csv'.format(league.upper(), season))

    else:  # Si no los hay
        print('No hay datos')

    return df_final


if __name__ == "__main__":
    p01 = getDF_picksBans('LEC', '2023')
    print(p01)
