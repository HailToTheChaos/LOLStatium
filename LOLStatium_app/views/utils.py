import pandas as pd
from io import StringIO
import datetime

def get_weeks_selector(df:pd.DataFrame):
    '''La función `get_weeks_selector` toma un DataFrame como entrada y devuelve una cadena HTML con
    opciones para seleccionar semanas.
    
    Parameters
    ----------
    df : pd.DataFrame
        El parámetro `df` es un DataFrame de pandas que contiene datos del jugador. Se supone que el
    DataFrame tiene una columna denominada "Semana" que representa el número de semana.
    
    Returns
    -------
        una cadena que contiene código HTML para un selector desplegable con opciones para semanas.
    
    '''
     #df de los jugadores sin duplicados
    df_weeks = df[['Week']].drop_duplicates()

    #Se inicializan las opciones del formulario, tanto de equipo como de jugadores
    weeks_select = '<option value=""></option>'

    #Se genera el html con todas las opciones de equipos y jugadores
    for index, row in df_weeks.iterrows():
      week = row['Week']
      weeks_select += '<option value="{}">{}</option>'.format(week,week)


    return weeks_select

def get_teams_selector(df:pd.DataFrame, type:str='',filt=False):
    '''La función `get_teams_selectors` genera opciones HTML para seleccionar equipos de un DataFrame
    determinado.
    
    Parameters
    ----------
    df : pd.DataFrame
        El parámetro `df` es un DataFrame de pandas que contiene los datos a partir de los cuales se
    generarán los selectores de equipo.
    type : str
        El parámetro "tipo" se utiliza para determinar el tipo de equipos a incluir en las opciones
    desplegables. Si "type" se establece en "topPicks", generará opciones para los equipos en la columna
    "Azul" del DataFrame "df". De lo contrario, generará opciones para
    
    Returns
    -------
        una cadena que contiene opciones HTML para un elemento seleccionado. Las opciones se generan en
    función del DataFrame de entrada y el parámetro de tipo. Si el tipo es 'topPicks', las opciones
    serán los valores únicos en la columna 'Azul' del DataFrame. De lo contrario, las opciones serán los
    valores únicos en la columna 'Equipo' del DataFrame.
    
    '''
    # Inicializo las opciones de los equipos  
    teams_select = ""
    if filt == False:        
        teams_select = '<option value=""></option>'
        
    if type == 'topPicks': # Para los topPicks
       # df de los equipos sin duplicados
        df_teams = df[['Blue']].drop_duplicates()

        for index, row in df_teams.iterrows():
          team = row['Blue']
          teams_select +=  '<option value="{}">{}</option>'.format(team,team)

    else: # Para el resto de vistas
        # df de los equipos sin duplicados
        df_teams = df[['Team']].drop_duplicates()

        for index, row in df_teams.iterrows():
            team = row['Team']
            teams_select +=  '<option value="{}">{}</option>'.format(team,team)

    return teams_select

def get_players_selector(df:pd.DataFrame, type:str=''):   
    '''La función `get_players_selector` genera un menú desplegable con nombres de jugadores basados en un
    tipo y marco de datos determinado.
    
    Parameters
    ----------
    df : pd.DataFrame
        El parámetro `df` es un DataFrame de pandas que contiene datos del jugador.
    type : str
        El parámetro "tipo" se utiliza para determinar el tipo de jugadores a seleccionar. Si "tipo" se
    establece en "topPicks", seleccionará a los mejores jugadores. De lo contrario, seleccionará a todos
    los jugadores.
    
    '''
    # Instancio las opciones de los jugadores con una opcion vacia
    players_select = '<option value=""></option>'

    if type=='topPicks':
        #<!--Serie con los nombres de los jugadores-->
        sr_players = df.filter(regex='^(BPPlayer|RPPlayer)[1-5]').stack().reset_index(name='nombres').loc[:,'nombres'].drop_duplicates()
        for row in sr_players:
            players_select += '<option value="{}">{}</option>'.format(row,row)

    else:
        # dataframe con los nombres de los jugadores sin duplicados
        df_teams = df[['Player']].drop_duplicates()

        for index, row in df_teams.iterrows():
            team = row['Player']
            players_select +=  '<option value="{}">{}</option>'.format(team,team)

    return players_select

def get_chart(fig):
    '''La función `get_chart` toma un objeto de figura, lo guarda como una imagen SVG y devuelve la imagen
    SVG como una cadena.
    
    Parameters
    ----------
    fig
        Se espera que el parámetro "fig" sea un objeto de figura matplotlib.
    
    Returns
    -------
        la imagen SVG del gráfico.
    
    '''
    # Creo el buffer
    buf = StringIO()
    # Guardo la figura en SVG
    fig.savefig(buf, format='svg')
    buf.seek(0)
    # Obtengo la imagen en SVG para mostrarla en el HTML
    image_svg = buf.getvalue()
    # Cierro el buffer
    buf.close()

    return image_svg