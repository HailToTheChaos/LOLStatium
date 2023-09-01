import json
import pandas as pd
import requests
from bs4 import BeautifulSoup
import bs4

principal = "https://lol.fandom.com"
# La lpl tiene su propia pagina para ver resultados
leagues = {'LCS': 8, 'LEC': 8, 'LCK': 9, 'LJL': 8, 'PCS': 5, 'VCS': 7}
splits = ('Winter_Season', 'Spring_Season', 'Summer_Season')
team_ids = {'AST': 'Astralis', 'BDS': 'Team BDS',
            'FNC': 'Fnatic', 'MAD': 'Mad Lions', 'MSF': 'Misfits Gaming'}

class Scraping:
    def getJson(enlace: str, TL: bool = False)->dict:        
        """
        Esta función toma una URL y un parámetro booleano opcional y devuelve un objeto JSON extraído
        del HTML de la URL, con la opción de agregar un parámetro de línea de tiempo a la URL.
        
        Args:
          enlace (str): una cadena que representa un enlace URL a una página web
          TL (bool): TL es un parámetro booleano que determina si agregar una acción específica a la
        URL. Si TL es True, la función agregará "/Timeline?action=edit" al final de la URL. Si TL es
        Falso, la función agregará "?acción=editar" al final de la URL. Defaults to False
        
        Returns:
          un diccionario (escriba `dict`).
        """
        if TL == True:  # Si el usuario ha puesto True
            # Se añade el TL
            enlace = f'{enlace}/Timeline?action=edit'
        else:
            enlace = f'{enlace}?action=edit'
        try:
            # hago una request al enlace
            response = requests.get(enlace)

            if (response.ok):
                # paso la request a texto para poder tratar con el
                html = response.text
                # extraigo el json contenido dentro de la etiqueta textArea del HTML
                json_finded = BeautifulSoup(html, 'html.parser').find('textarea')
                # genero el json, pasando el objeto anterior a string y quitandole los espacios
                # del principio y del final. Devuelvo el JSON generado
                return json.loads(json_finded.string.strip())

        # Error de conexion
        except (requests.ConnectionError):
            print("Error de conexión")

        # Error de url no valida
        except (ValueError):
            print("Error de formato de URL")

    def getChampionById(key: int):
        url = "http://ddragon.leagueoflegends.com/cdn/13.6.1/data/en_US/champion.json"
        response = requests.get(url)
        data = response.json()

        for champion, details in data['data'].items():
            if details['key'] == str(key):
                return details['id']

    def getParticipantByIdV5(json_data: dict, id: int) -> str:
        """Método para obtener el nombre de jugador a través del ID 

        Args:
            json_data (dict): Json con todos los datos de la partida
            id (str): ID del jugador

        Returns:
            str: Nombre del jugador
        """        
        # Se obtiene el nodo de participantes del JSON
        participants = json_data['participants']

        for participant in participants:
            if participant['participantId'] == id:          
                return participant['summonerName']
            
    def getParticipantByIdV4(json_data: dict, id: int) -> str:
        """Método para obtener el nombre de jugador a través del ID 

        Args:
            json_data (dict): Json con todos los datos de la partida
            id (str): ID del jugador

        Returns:
            str: Nombre del jugador
        """        
        # Se obtiene el nodo de participantes del JSON
        participants = json_data['participantIdentities']

        for participant in participants:
            if participant['participantId'] == id:          
                return participant['player']['summonerName']

    def games(league: str, season: str)->list[list:str,list:str,list:str,list:str,list:str]:
        """
        La función "juegos" recupera datos de un sitio web para una liga y temporada determinada, y devuelve
        una lista de nombres divididos, semanas, equipos azules, equipos rojos y enlaces a datos del juego.
        
        Args:
          league (str): una cadena que representa el nombre de una liga/región
          season (str): El parámetro de temporada es una cadena que representa la temporada específica de
        una liga de la que el usuario desea recuperar datos.
        
        Returns:
          una lista de cinco listas: splits, semanas, blueTeams, redTeams y out.
        """
        # Se inicializan las listas para guardar los datos
        splts = []
        weeks = []
        out = []
        blueTeams = []
        redTeams = []
        if league in leagues:  # Se comprueba que exista esa liga/región
            try:
                # Se itera las seasons
                for i in range(len(splits)):
                    # Se hace la consulta a la página
                    response = requests.get(
                        f'{principal}/{league}/{season}_Season/{splits[i]}')

                    if (response.ok):  # Se comprueba que se puede acceder a la página
                        # Se obtiene el HTML de la página
                        soup = BeautifulSoup(response.text, 'html.parser')
                        # Se extrae la tabla de la página
                        table = soup.find('table', {'id': 'md-table'})
                        # Se obtienen todos los links de la tabla
                        links = table.find_all(
                            'a', href=True, target=False, string='Link')

                        # Se controla si hay datos en la tabla
                        if links != []:
                            aux = blueRedTeams(table, league)
                            # Extiendo las listas con los datos nuevos
                            blueTeams.extend(aux[0])
                            redTeams.extend(aux[1])
                            weeks.extend(getWeeks(table))
                            substring = 'meta'
                            # Se iteran los enlaces
                            for link in links:
                                splts.append(splits[i].split('_')[0])
                                # Se extrae el link de la tabla
                                new_link = link['href'].replace(substring, '')

                                out.append(f'{principal}{new_link}')

            # Error de conexion
            except (requests.ConnectionError):
                print("Error de conexión")

            # Error de url no valida
            except (ValueError):
                print("Error de formato de URL")

        else:
            print('Región no válida')

        return splts, weeks, blueTeams, redTeams, out


def blueRedTeams(table:bs4.element.Tag, league:str)->list[list,list]:   
    """
    La función toma una tabla y una liga como entrada y devuelve dos listas de equipos azul y rojo
    respectivamente.
    
    Args:
      table (bs4.element.Tag): La tabla HTML que contiene los nombres de los equipos y la información de
    los partidos.
      league (str): El nombre de la liga para la que se analiza la tabla.
    
    Returns:
      una lista de dos listas, donde la primera lista contiene los nombres de los equipos azules y la
    segunda lista contiene los nombres de los equipos rojos.
    """
    blueTeams = []
    redTeams = []
    rows = table.find_all("tr")

    if len(rows) >=2:
        blueCol = leagues[league]
        for row in rows:
            cols = row.find_all("td")
            
            if cols != []:
                #Para tablas que están por BO3
                if 'multirow-highlighter mdv-allweeks mdv-week1' in row.get('class', []):
                    blueTeams.append(cols[blueCol].text)
                    redTeams.append(cols[blueCol + 1].text)
                else:
                    blueTeams.append(cols[0].text)
                    redTeams.append(cols[1].text)    

    return blueTeams, redTeams

def getWeeks(table:bs4.element.Tag)->list:
    """
    La función extrae los nombres de las semanas de una tabla HTML utilizando Beautiful Soup.
    
    Args:
      table (bs4.element.Tag): un objeto de etiqueta BeautifulSoup que representa una tabla HTML.
    
    Returns:
      una lista de cadenas, que son los nombres de las semanas en una tabla.
    """
    weeks = []
    rows = table.find_all("tr")
    
    if len(rows) >=2:
      #Se recorren las filas
        for row in rows:
          #Se obtienen los titulos de las columnas
            th = row.find('th')
            if th != None:
              #Si en los títulos aparecen los nombres de Week o Tiebreakers se guardan en la variable
                if 'Week' in th.text:
                    week = th.text.split(']')[1]
                elif 'Tiebreakers' in th.text:
                    week = th.text.split(']')[1]
            else:
              #Si no aparecen dichos nombres, se va guardando el nombre de la semana
                weeks.append(week)

    return weeks 