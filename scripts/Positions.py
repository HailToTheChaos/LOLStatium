import pandas as pd
from Web_scrap import *
from tqdm import tqdm
import math
import json


def getEvents(json_data: dict) -> dict:
    """Método para obtener los eventos del json de las partidas

    Args:
        json_data (dict): json del Timeline del juego en una partida

    Returns:
        dict: json con todos los eventos
    """
    person = json_data['frames']
    event = person[0]['events']
    for i in range(1, len(person)):
        event += person[i]['events']

    return event


def getParticipantFrames(json_data: dict) -> dict:
    """Método para obtener los Frames de los participantes del json de la partida

    Args:
        json_data (dict): json del Timeline del juego en una partida

    Returns:
        dict: json con los participantFrames
    """
    person = json_data['frames']
    pFrames = []
    for i in range(len(person)):
        pFrames.append(person[i]['participantFrames'])
    return pFrames


def findKills(split: str, week: str, events: dict, json_data: dict) -> pd.DataFrame:
    """Método para encontrar los asesinatos que se especifican en el json

    Args:
        split (str): Split de la partida
        week (str): Semana de la partida
        events (dict): json con los eventos
        json_data (dict): Json con los datos de la partida

    Returns:
        pd.DataFrame: DataFrame con las kills
    """
    df_eventos = pd.DataFrame(events)
    # Se hace una query en el DF para buscrar las kills y special kills
    df_eventos = df_eventos.query(
        "type == 'CHAMPION_KILL' or type == 'CHAMPION_SPECIAL_KILL'").reset_index()

    # Se guardan los IDs como numeros enteros en una lista
    killerIds = df_eventos['killerId'].astype(int).values.tolist()

    players = []
    teams = []

    
    # Se recorren los ids
    for i in range(0, len(killerIds)):
        # Se guardan los nombres
        if killerIds[i] != 0:
            try:  # Para V5
                killerName = Scraping.getParticipantByIdV5(
                    json_data, killerIds[i])
            except KeyError:  # Para V4
                killerName = Scraping.getParticipantByIdV4(
                    json_data, killerIds[i])

            players.append(killerName.split(' ')[1])
            teams.append(killerName.split(' ')[0])

        else:
            players.append('-')
            teams.append('-')


    ejeX = []
    ejeY = []

    df_final = pd.DataFrame()
    if not df_eventos.empty:
        # Se obtiene la posición y la añadimos a la ultima posición de los diccionarios
        for i in range(len(df_eventos['position'])):
            df_posicion = df_eventos['position'][i]
            if df_eventos['killerId'][i] <= 5:
                ejeX.append(df_posicion.get('x'))
                ejeY.append(df_posicion.get('y'))

            # Si está en el equipo rojo se le invierten las coordenadas
            else:
                ejeX.append(df_posicion.get('y'))
                ejeY.append(df_posicion.get('x'))

        # Se pasa a DataFrame
        df_final = pd.DataFrame(
            {'Team': teams, 'Player': players, 'X': ejeX, 'Y': ejeY})
        df_final.insert(0, 'Split', split)
        df_final.insert(1, 'Week', week)

    return df_final


def findFirstBloodV5(split: str, week: str, events: dict, json_data: dict) -> pd.DataFrame:
    """Método para obtener un DataFrame con las primeras sangres de cada partida

    Args:
        split (str): Split de la partida
        week (str): Semana de la partida
        events (dict): json con los eventos
        json_data (dict): Json con los datos de la partida

    Returns:
        pd.DataFrame: DataFrame con las First blood
    """

    # Recorremos los eventos
    for event in events:
        # Buscamos la First Blood y lo devolovemos en forma de DF
        if event.get('killType') == 'KILL_FIRST_BLOOD':
            # Se guarda la posición
            position = event['position']

            participantId = event['killerId']
            # Se obtiene el nombre del jugador
            killer = Scraping.getParticipantByIdV5(json_data, participantId)
            # Se devuelve un Dataframe con los datos
            if participantId <= 5:
                return pd.DataFrame({'Split': split, 'Week': week, 'Team': killer.split(' ')[0], 'Player': killer.split(' ')[1], 'X': position['x'], 'Y': position['y']}, index=[0])

            else:
                return pd.DataFrame({'Split': split, 'Week': week, 'Team': killer.split(' ')[0], 'Player': killer.split(' ')[1], 'X': position['y'], 'Y': position['x']}, index=[0])


def findDeaths(split: str, week: str, participantFrames: dict, json_data: dict) -> pd.DataFrame:
    """Método para encontrar las muertes de los jugadores de una partida

    Args:
        split (str): Split de la partida
        week (str): Semana de la partida
        participantFrames (dict): Frames de los participantes de la partida
        json_data (dict): Json con los datos de la partida

    Returns:
        pd.DataFrame: DataFrame con las posiciones de las muertes
    """
    positions = []
    for i in range(len(participantFrames)):
        # Recorremos los frames de los participantes
        for participant_id, participant_data in participantFrames[i].items():
            if participant_data['championStats']['health'] == 0:
                # Si la salud es 0 se guardan el nombre del jugador y la posición
                player = Scraping.getParticipantByIdV5(
                    json_data, int(participant_id))
                position = participant_data['position']
                # Guardamos en una lista los diccionarios
                if int(participant_id) <= 5:
                    positions.append(
                        {'Split': split, 'Week': week, 'Team': player.split(' ')[0], 'Player': player.split(' ')[1], 'X': position['x'], 'Y': position['y']})
                else:  # Si están en el equipo rojo se le invierten las coordenadas
                    positions.append(
                        {'Split': split, 'Week': week, 'Team': player.split(' ')[0], 'Player': player.split(' ')[1], 'X': position['y'], 'Y': position['x']})
    # Creamos un dataFrame a partir de la lista y lo devolvemos
    return pd.DataFrame(positions)


def findWards(split: str, week: str, events: dict, participantFrames: dict, json_data: dict) -> dict:
    """Método para buscar las posiciones de los wards colocados por los jugadores en una partida

    Args:
        events (dict): Json con los eventos

    Returns:
        dict: DataFrame de los wards colocados
    """

    participantId = []
    timeStamp = []
    calculo = 60000
    for event in events:
        if event.get('type') == 'WARD_PLACED':
            participantId.append(event.get('creatorId'))
            timeStamp.append(event.get('timestamp'))
    timeStamp = list(map(lambda x: math.ceil(x / calculo), timeStamp))
    posiciones = []
    teams = []
    players = []
    for i in range(len(participantId)):
        if (participantId[i] > 0):
            posiciones.append(participantFrames[timeStamp[i]].get(
                str(participantId[i])).get('position'))
            try:
                player = Scraping.getParticipantByIdV5(
                    json_data, participantId[i])

            except KeyError:
                player = Scraping.getParticipantByIdV4(
                    json_data, participantId[i])

            teams.append(player.split(' ')[0])
            players.append(player.split(' ')[1])
    x = []
    y = []
    for i in range(len(posiciones)):
        if participantId[i] <= 5:
            x.append(posiciones[i].get('x'))
            y.append(posiciones[i].get('y'))

        else:
            x.append(posiciones[i].get('y'))
            y.append(posiciones[i].get('x'))

    df_wards = pd.DataFrame(
        {'Split': split, 'Week': week, 'Team': teams, 'Player': players, 'X': x, 'Y': y})
    return df_wards


def getDF_positions(league: str, season: str, download: bool = False) -> pd.DataFrame:
    """Función para sacar las posiciones de Kills, Deaths, FirstBlood y Wards

    Args:
        league (str): Liga a buscar
        season (str): Año de liga
        download (bool): Descarga en formato .csv

    Returns:
        pd.DataFrame: DataFrame con las posiciones
    """
    df_final = pd.DataFrame()
    if league in leagues and season !='' and season.isdigit:
        # Se obtienen los datos de la season
        data = Scraping.games(league.upper(), season)

        # Se guardan los datos de la season en variables
        splits = data[0]
        weeks = data[1]
        BlueTeams = data[2]
        RedTeams = data[3]
        links = data[4]

        # Se crean los DataFrames vacios de las posiciones divididos por tipos
        df_firstblood = pd.DataFrame()
        df_deaths = pd.DataFrame()
        df_kills = pd.DataFrame()
        df_wards = pd.DataFrame()

        # Se recorren las partidas de la season
        for i in tqdm(range(0, len(links)), unit='MB',colour='Red', desc=f'Positions Kills, deaths & first blood. {league} {season}', leave=False):
            # Se obtiene el json con el time line de la partida
            json_timeline = Scraping.getJson(links[i], TL=True)
            # Se obtiene el Json con los datos de la partida
            json_data = Scraping.getJson(links[i])
            # Se obtienen todos los frames de los participantes de la partida
            pFrames = getParticipantFrames(json_timeline)
            # Se obtienen todos los eventos de la partida
            events = getEvents(json_timeline)

            # Se concatenan las posiciones de los asesinatos
            df_kills = pd.concat([df_kills, findKills(splits[i], weeks[i],
                                                      events, json_data)], ignore_index=True)

            if 'V5' in links[i]:  # Solo para la versión 5 de los datos obtenidos en lol.fandom.com
                # Se concatenan las posiciones de las primeras sangres
                df_firstblood = pd.concat(
                    [df_firstblood, findFirstBloodV5(splits[i], weeks[i], events, json_data)], ignore_index=True)

                # Se concatenan las posiciones de los Wards colocados
                df_wards = pd.concat([df_wards, findWards(
                    splits[i], weeks[i], events, pFrames, json_data)], ignore_index=True)

                # Se concatenan las posiciones de las muertes
                df_deaths = pd.concat([df_deaths, findDeaths(splits[i], weeks[i],
                                                             pFrames, json_data)], ignore_index=True)

            elif 'V4' in links[i]:
                # Se concatenan las posiciones de las primeras sangres
                df_firstblood = pd.concat(
                    [df_firstblood, df_kills.iloc[:1]], ignore_index=True)

        # Se insertan los tipos
        df_kills.insert(2, 'Type', 'Kill')
        df_firstblood.insert(2, 'Type', 'FirstBlood')
        df_deaths.insert(2, 'Type', 'Death')
        df_wards.insert(2, 'Type', 'Ward')

        # Se crea un DataFrame global con todas las posiciones
        df_final = pd.concat(
            [df_kills, df_firstblood, df_deaths, df_wards], ignore_index=True)
        
        df_final.insert(0,'Season',season)

        # Se crea el csv
        if download:
            df_final.to_csv(
                'Model\\Download\\Positions-{}_{}.csv'.format(league.upper(), season), index=False)
            print('Model\\Datos guardados en: Download\\Positions-{}_{}.csv'.format(league.upper(), season))

        # Devolvemos el DataFrame
    return df_final


if __name__ == "__main__":
    dato = getDF_positions('LEC', '2023')
    print(dato)
