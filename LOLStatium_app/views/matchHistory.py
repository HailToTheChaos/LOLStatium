from django.shortcuts import render
from django.http import JsonResponse

from .utils import *
import pandas as pd
from LOLStatium_app.models import MatchHistory, Match
import datetime

df = pd.DataFrame()


def matchs(request, season=datetime.datetime.now().date().year):
    """
    La función `matchs` recupera datos de coincidencias de una base de datos, los formatea en un
    DataFrame y los representa en una plantilla HTML.
    
    :param request: El objeto de solicitud representa la solicitud HTTP que realizó el usuario para
    acceder a la vista
    :param season: El parámetro "temporada" es un parámetro opcional que especifica la temporada para la
    que se solicitan los datos del historial de partidos. Si no se proporciona ninguna temporada, el
    valor predeterminado es el año actual obtenido de la función `datetime.datetime.now().date().year`
    :return: una plantilla HTML renderizada con los datos de contexto.
    """
    # Obtengo los modelos de la base de datos de Django
    match = pd.DataFrame(MatchHistory.objects.filter(
        Match__Season=season).values())
    matchData = pd.DataFrame(Match.objects.filter(Season=season).values())

    # Lo convierto a Dataframe
    df = pd.merge(matchData, match, on='Match_id')

    df = df.rename({'Player': 'Jugador', 'championName': 'Campeón',
                   'Gold': 'Oro', 'Gold/Damage': 'Oro/Daño'}, axis=1)
    
    # Invierto el dataframe para que se vean los registros más recientes antes
    df_invertido = df[::-1].copy()

    paneles = []
    for i in range(0, len(df_invertido), 10):
        split = df_invertido['Split'].iloc[i]
        week = df_invertido['Week'].iloc[i]
        teams = f"{df_invertido['Blue'].iloc[i]} - {df_invertido['Red'].iloc[i]}"

        # Header de cada tabla
        text_game = f"Split: {split} | Week: {week} | Game: {teams}"
        game = f'<h2>{text_game}</h2>'
        paneles.append(game)

        # Dataframe con los datos. Se pasan a HTML.
        paneles.append(df_invertido.iloc[i:i+10].drop(
            ['Match_id', 'id', 'Season', 'Split', 'Week'], axis=1).to_html(border=0, index=False))

    context = {
        'year': season,
        'semanas': get_weeks_selector(df),
        'equipos': get_teams_selector(df, 'matchs'),
        'paneles': paneles,
    }

    return render(request, 'matchHistory.html', context)


# <!--Función que al cambiar la selección del equipo, muestra los jugadores de ese equipo.-->
def onChangingSelectedWeek(request):
    if request.method == 'POST' and request.is_ajax():
        ts = request.POST.get('week-select')
        if ts:
            df_filt = df[df.Week == ts][['Team']].drop_duplicates()
            ps = '<option value=""></option>'
            for index, row in df_filt.iterrows():
                ps += '<option value="{}">{}</option>'.format(
                    row['Team'], row['Team'])

            return JsonResponse({'game_options': ps})

        return JsonResponse({'game_options': ''})


# #<!--Función para filtrar los datos leyendo el formulario-->
# def filterData():
#   #<!--Se guardan los valores de las etiquetas-->
#   game = js.document.getElementById('game-select').value
#   week = js.document.getElementById('week-select').value
#   split = js.document.getElementById('split-select').value

#   query = []
#   filt = False
#   df_filt = df
#   #Se guarda la consulta al dataframe
#   if game != '':
#     query.append(f"Game == '{game}'")
#     filt = True

#   if week != '':
#     query.append(f"Week == '{week}'")
#     filt = True

#   if split != '':
#     query.append(f"Split == '{split}'")
#     filt = True
#   if filt:
#     #Se hace la consulta
#     df_filt = df.query(" and ".join(query))

#   # Actualizar el mapa de calor
#   out = matchHistory(df_filt)

#   # Actualizar el panel con los datos filtrados
#   pane.object = matchHistory(df_filt)

# #<!--Función para limpiar el filtro-->
# def clearFilters():
#   #<!--Se guardan los valores de las etiquetas-->
#   split = js.document.getElementById('split-select').value
#   week = js.document.getElementById('week-select').value
#   game = js.document.getElementById('game-select').value

#   if not(split and week and game == ''):
#     #Se establecen los valores de las etiquetas del formulario a vacio
#     js.document.getElementById('game-select').value = ''
#     js.document.getElementById('week-select').value = ''
#     js.document.getElementById('split-select').value = ''

#     # Actualizar el panel con los datos filtrados
#     pane.object = matchHistory(df)
