import pandas as pd
from Web_scrap import Scraping
from Web_scrap import *
from tqdm import tqdm
import requests
from os import system

# Assign URL
principal = "https://lol.fandom.com/"

def getChampionId()->tuple[list]:
    """
    Esta función recupera una lista de claves e ID de campeones de la API de League of Legends.
    
    Returns:
      una tupla que contiene dos listas: la primera lista contiene las claves de todos los campeones del
    juego League of Legends y la segunda lista contiene los ID de todos los campeones del juego.
    """
    lista = []
    lista2 = []
    url = "http://ddragon.leagueoflegends.com/cdn/13.6.1/data/en_US/champion.json"
    response = requests.get(url)
    data = response.json()
    for champion, details in data['data'].items():
        lista.append(details['key'])
        lista2.append(details['id'])
    return lista, lista2

def winLost(json:dict)->pd.DataFrame:
    """
    La función toma un objeto JSON que contiene datos sobre un juego de League of Legends y devuelve un
    DataFrame de pandas con información sobre el rendimiento de cada jugador en el juego, incluido su
    registro de victorias/derrotas, asesinatos, muertes, asistencias y campeón jugado.
    
    Args:
      json (dict): El parámetro de entrada es un diccionario llamado "json" que contiene información
    sobre un juego de League of Legends. La función procesa esta información y devuelve un DataFrame de
    pandas que contiene estadísticas sobre los jugadores en el juego.
    
    Returns:
      un marco de datos de pandas con columnas para ChampionName, SumerName, gameId, juegos, Win, loss,
    kills, death, assists y teamId. Los datos en DataFrame se basan en el diccionario JSON de entrada,
    que se espera que contenga información sobre un juego de League of Legends. La función primero
    intenta extraer los datos necesarios asumiendo que el JSON está en un formato determinado, y
    """
    person = json['participants']
    try:
        for i in range(10):
            person[i]['gameId'] = json['gameId']
            if ('games' in person):
                person[i]['games'] = person[i]['games']+1
            else:
                person[i]['games'] = 1
            if (person[i]['win'] == True):
                if ('Win' in person):
                    person[i]['Win'] = person[i]['Win']+1
                else:
                    person[i]['Win'] = 1
                    person[i]['lose'] = 0
            else:
                if ('lose' in person):
                    person[i]['lose'] = person[i]['lose']+1
                else:
                    person[i]['lose'] = 1
                    person[i]['Win'] = 0
        pan = pd.DataFrame(person)
        return pan[['championName', 'summonerName', 'gameId', 'games', 'Win', 'lose', 'kills', 'deaths', 'assists', 'teamId']]

    except KeyError: #En el caso de que los datos sean V4
        datos = json['participantIdentities']

        for i in range(10):
            person[i]['summonerName'] = datos[i]['player']['summonerName']
            person[i]['championName'] = Scraping.getChampionById(
                person[i]['championId'])
            person[i]['kills'] = person[i]['stats']['kills']
            person[i]['deaths'] = person[i]['stats']['deaths']
            person[i]['assists'] = person[i]['stats']['assists']
            person[i]['gameId'] = json['gameId']

            if ('games' in person):
                person[i]['games'] = person[i]['games']+1
            else:
                person[i]['games'] = 1

            if (person[i]['stats']['win'] == True):
                if ('Win' in person):
                    person[i]['Win'] = person[i]['Win']+1
                else:
                    person[i]['Win'] = 1
                    person[i]['lose'] = 0
            else:
                if ('lose' in person):
                    person[i]['lose'] = person[i]['lose']+1
                else:
                    person[i]['lose'] = 1
                    person[i]['Win'] = 0

        pan = pd.DataFrame(person)

        return pan[['championName', 'summonerName', 'gameId', 'games', 'Win', 'lose', 'kills', 'deaths', 'assists', 'teamId']]

def bansCont(json:dict, data:pd.DataFrame)->pd.DataFrame:
    """
    La función toma un objeto JSON y un DataFrame de Pandas, itera a través del objeto JSON para extraer
    las prohibiciones de campeones y su turno de selección para cada equipo, agrega una nueva columna al
    DataFrame que indica si un campeón fue prohibido o no, y actualiza el "Promedio". BT" en el
    DataFrame con el turno de selección de cada campeón prohibido antes de devolver un subconjunto del
    DataFrame con solo los campeones prohibidos y su turno de selección.
    
    Args:
      json (dict): Un diccionario que contiene información sobre un juego de League of Legends,
    incluidos los equipos y las prohibiciones de sus campeones.
      data (pd.DataFrame): Un DataFrame de pandas que contiene información sobre campeones en un juego
    de League of Legends.
    
    Returns:
      un DataFrame de pandas que incluye el nombre del campeón, si fueron baneados o no (1 para baneado,
    0 para no baneado) y el turno de baneo promedio para cada campeón baneado. El DataFrame solo incluye
    filas donde el campeón fue baneado.
    """
    person = json['teams']
    lista = []
    listaT = []
    # Iterar a través de la lista de equipos
    for team in person:
        # Iterar a través de su lista de selecciones de campeones
        for ban in team['bans']:
            champion_name = Scraping.getChampionById(ban['championId'])
            lista.append(champion_name)
            listaT.append(ban['pickTurn'])
    data["ban"] = data.championName.isin(lista)
    data["ban"] = data.ban.replace({True: 1, False: 0})
    # data['gameId']=json['gameId']
    for i in range(len(lista)):
        pd.set_option('display.max_rows', None)
        num = data.index[data['championName'] == lista[i]].tolist()
        data.at[num[0], 'Avg BT'] = listaT[i]
    return data.loc[data['ban'] > 0, ['championName', "ban", "Avg BT"]]


def kda(data:pd.DataFrame)->pd.DataFrame:
    """
    La función toma un DataFrame de pandas de los datos de los partidos de League of Legends y devuelve
    un DataFrame modificado con columnas adicionales para KDA, tasa de victorias y otras estadísticas
    agrupadas por jugador y campeón.
    
    Args:
      data (pd.DataFrame): El marco de datos de entrada que contiene datos sobre los partidos de League
    of Legends.
    
    Returns:
      un marco de datos de pandas con columnas para el nombre del jugador, el equipo, el lado, la
    división, la cantidad de juegos jugados, el nombre del campeón, la clave del campeón, la cantidad de
    victorias y derrotas, la cantidad de muertes, asistencias y muertes tanto para el jugador como para
    el campeón, recuento de bloqueos, BT promedio (variable desconocida), tasa de ganancias y KDA tanto
    para el jugador como para el campeón.
    """
    agrupado = data.groupby(['championName', 'key']).agg(
        {'games': 'count', 'ban': 'sum', 'Win': 'sum', 'lose': 'sum', 'kills': 'sum',
         'assists': 'sum', 'deaths': 'sum'}).reset_index()
    data = pd.merge(data, agrupado, on=['championName', 'key'])
    data = data.rename(columns={"games_y": "games", "deaths_y": "deathsC",
                       'assists_y': 'assistsC', 'kills_y': 'killsC', "deaths_x": "deaths"})
    data = data.rename(columns={'assists_x': 'assists', 'kills_x': 'kills',
                       "Win_y": "Win", "lose_y": "lose", 'ban_y': 'ban'})
    data.loc[data['deathsC'] > 0, 'kda'] = (
        data['killsC']+data['assistsC'])/data['deathsC']
    data.loc[data['deathsC'] < 1, 'kda'] = (data['killsC']+data['assistsC'])
    data['wR'] = data['Win']/data['games']
    data["Side"] = ["Red" if s > 100 else "Blue" for s in data['teamId']]
    try:
        data[['team', 'summonerName', 'c']
             ] = data.summonerName.str.split(' ', expand=True)
    except:
        data[['team', 'summonerName']] = data.summonerName.str.split(
            ' ', expand=True)
    data = data.rename(
        columns={"summonerName": "Player", "championName": "Champion"})
    agrupado = data.groupby(['Player', 'Split']).agg(
        {'kills': 'sum', 'assists': 'sum', 'deaths': 'sum'}).reset_index()
    data = pd.merge(data, agrupado, on=['Player', 'Split'])
    data = data.rename(columns={"deaths_y": "deathsJ", 'assists_y': 'assistsJ', 'kills_y': 'killsJ',
                       "deaths_x": "deaths", 'assists_x': 'assists', 'kills_x': 'kills', 'kda': 'kdaC'})
    data.loc[data['deathsJ'] > 0, 'kda'] = (
        data['killsJ']+data['assistsJ'])/data['deathsJ']
    data.loc[data['deathsJ'] < 1, 'kda'] = (data['killsJ']+data['assistsJ'])
    return data[['Player', 'team', 'Side', 'Split', 'games', 'Champion', 'key', 'Win', 'lose', 'kills', 'assists', 'deaths', 'killsC', 'assistsC', 'deathsC', 'killsJ', 'assistsJ', 'deathsJ', 'kda', 'kdaC', 'ban', 'Avg BT', 'wR']]


def presence(datos):
    datos['Presence'] = ((datos['ban']+datos['games']) /
                         (datos['games']. max()+datos['ban']. max()))*100
    return datos


def metaDat(tabla:pd.DataFrame, json:dict, split:str)->pd.DataFrame:
    """
    La función toma un DataFrame, un diccionario y una cadena como entradas, realiza algunas operaciones
    en ellos y devuelve un nuevo DataFrame.
    
    Args:
      tabla (pd.DataFrame): Un DataFrame de pandas que contiene datos sobre campeones en una liga o
    torneo en particular.
      json (dict): Es un diccionario que contiene datos relacionados con los partidos de League of
    Legends, como selecciones y prohibiciones de campeones, estadísticas de jugadores y resultados de
    juegos.
      split (str): El parámetro "split" es una cadena que representa la temporada actual o el período de
    tiempo en una liga o torneo competitivo. Se utiliza para etiquetar los datos en el DataFrame
    devuelto.
    
    Returns:
      un DataFrame de pandas llamado "metaf".
    """
    data = winLost(json)
    data = data.sort_values(by='championName')
    dato = pd.merge(tabla, data)
    dato = dato.assign(Split=split)
    dato2 = bansCont(json, tabla)
    metaf = pd.concat([dato, dato2], axis=0)
    return metaf


def getDF_metaData(league:str, season:str, download:bool=False)->pd.DataFrame:
    """
    Esta función recupera los metadatos de una liga y una temporada determinadas y, opcionalmente, los
    descarga como un archivo CSV.
    
    Args:
      league (str): una cadena que representa el nombre de la liga de League of Legends para la que
    desea recuperar los metadatos.
      season (str): Una cadena que representa la temporada para la que se recuperan los metadatos.
      download (bool): Un parámetro booleano que indica si descargar el DataFrame resultante como un
    archivo CSV o no. Si se establece en True, la función guardará el DataFrame como un archivo CSV en
    la carpeta "Descargar". Si se establece en False, la función solo devolverá el DataFrame sin
    guardarlo. Defaults to False
    
    Returns:
      un DataFrame de pandas que contiene metadatos para una liga y una temporada determinadas, con
    opciones para descargar los datos como un archivo CSV.
    """
    result = pd.DataFrame()
    if league in leagues:
        tabla = pd.DataFrame()
        dat = getChampionId()
        tabla['championName'] = dat[1]
        tabla['key'] = dat[0]
        data = Scraping.games(league.upper(), season)
        split = data[0]
        links = data[4]
        df_final = pd.DataFrame()
    
        for i in tqdm(range(0, len(links)), unit='MB', desc=f'MetaDatos {league} {season}', colour='Magenta', leave=False):
            df_final = pd.concat(
                [df_final, metaDat(tabla, Scraping.getJson(links[i]), split[i])])
            
        pd.set_option('display.max_rows', None)
        result = df_final.sort_values(
            by=['championName'], ascending=False).reset_index().drop(['index'], axis=1)
        result = kda(result)
        result = presence(result)
        result = (result.sort_values(
            by=['Presence'], ascending=False).reset_index().drop(['index'], axis=1))
        
        result.insert(0,'Season',season)
    
        # Se crea el csv
        if download:
            result.to_csv(
                f'Model\\Download\\Meta-{league.upper()}_{split}.csv', index=False)
            print('Datos guardados en: Model\\Download\\Meta-{}_{}.csv'.format(league.upper(), split))

    return result


if __name__ == "__main__":
    p01 = getDF_metaData('LEC', '2023')
    print(type(p01['Win'][0]))

# Gracias a la persona que hizo este código, estoy desarrollando mucha paciencia