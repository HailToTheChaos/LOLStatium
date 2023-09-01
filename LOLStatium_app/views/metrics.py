from django.shortcuts import render
from .utils import *
import pandas as pd
import datetime
from LOLStatium_app.models import MetaData

current_year = datetime.datetime.now().date().year

def metadata(request, season=current_year):
     # Obtengo los modelos de la base de datos de Django
    query = MetaData.objects.filter(Season=season)
    query = query.values('Player', 'Team', 'Split', 'KDA', 'WR').distinct('Player')
    df = pd.DataFrame(query)
    df['WR'] = df['WR'] * 100
    df = df.round(2)
    df_rename = df.rename(columns={
                          'Player': 'Jugador', 'Team': 'Equipo', 'Season': 'Temporada', 'WR': 'Win rate (%)'})

    # #Se crea la tabla a través del DF
    html_tabla = df_rename.to_html(border=0, index=False)
    context = {
        'year': season,
        'equipos': get_teams_selector(df),
        'jugadores': get_players_selector(df),
        'tabla': html_tabla,
    }

    return render(request, 'metrics.html', context)

    # #Función que al cambiar la selección del equipo, muestra los jugadores de ese equipo.
    # def onChangingSelectedTeam():
    #   ts = Element('team-select').value
    #   if ts != '':
    #     js.document.getElementById('player-select').innerHTML = ''
    #     df_filt = df[df.team==ts][['Player']].drop_duplicates()
    #     ps = '<option value=""></option>'
    #     for index, row in df_filt.iterrows():
    #       ps = ps + '<option value="{}">{}</option>'.format(row['Player'],row['Player'])
    #     js.document.getElementById('player-select').innerHTML = ps
    #   else:
    #     js.document.getElementById('player-select').innerHTML = players
    # #Función para filtrar los datos leyendo el formulario
    # def filterData():
    #   #Se guardan los valores de las etiquetas
    #   team = js.document.getElementById('team-select').value
    #   player = js.document.getElementById('player-select').value
    #   season = js.document.getElementById('Season-select').value

    #   query = []
    #   filt = False
    #   #Se guarda la consulta al dataframe
    #   if team != '':
    #     query.append(f"Equipo == '{team}'")
    #     filt = True
    #   if player != '':
    #     query.append(f"Jugador.str.contains(@player)")
    #     filt = True

    #   if season != '':
    #     query.append(f"Split == '{season}'")
    #     filt = True
    #   if filt:
    #     #Se hace la consulta
    #     df_filt = df_rename.query(" and ".join(query))
    #     #Se actualiza la tabla con los nuevos datos
    #     pane_df.object = df_filt

    # #Función para limpiar el filtro
    # def clearFilters():
    #   #Se establecen los valores de las etiquetas del formulario a vacio
    #   js.document.getElementById('player-select').value = ''
    #   js.document.getElementById('team-select').value = ''
    #   js.document.getElementById('Season-select').value = ''
    #   #Se restablece la tabla
    #   pane_df.object = df_rename

    # def toggle_filter_menu():
    #   menu = js.document.getElementById("filter-menu")
    #   if menu.style.display == "none":
    #     menu.style.display = "block"
    #   else:
    #     menu.style.display = "none"

    # def toggle_menu():
    #   menu = js.document.getElementById("menu")
    #   if menu.style.display == "none":
    #     menu.style.display = "block"
    #   else:
    #     menu.style.display = "none"

    # def upDown():
    #   #Se guardan los valores de las etiquetas
    #   tipo = js.document.getElementById('type-select').value
    #   asc = js.document.getElementById('asc-select').value

    #   if asc == 'Ascendente':
    #     ascendente = True
    #   elif asc == 'Descendente':
    #     ascendente = False

    #   if tipo:
    #     df_sorted = df_rename.sort_values(by=tipo, ascending=ascendente)
    #     pane_df.object = df_sorted

    # def clearUpDown():
    #   #Se guardan los valores de las etiquetas
    #   tipo = js.document.getElementById('type-select').value

    #   if tipo:
    #     js.document.getElementById('type-select').value = ''
    #     pane_df.object = df_rename
