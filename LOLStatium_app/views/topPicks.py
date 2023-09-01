# Django
from django.shortcuts import render
from LOLStatium_app.models import PicksBans
from LOLStatium_app.models import Match
from django.http import JsonResponse

from .utils import *

# Libs
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import requests

year = datetime.datetime.now().date().year
# <!--Link de la API de ddragon con las imágenes de los campeones-->
link = r'http://ddragon.leagueoflegends.com/cdn/13.9.1/img/champion/'


def topPick(request, season=year):
    # Se lee la Query a la base de datos y se transforma en DF
    picks = pd.DataFrame(PicksBans.objects.filter(
        Match__Season=season).values())
    matchs = pd.DataFrame(Match.objects.filter(Season=season).values())

    df = pd.merge(picks, matchs, on='Match_id')
    table = topPickBan(df)

    context = {
        'year': season,
        'equipos': get_teams_selector(df, 'topPicks'),
        'jugadores': get_players_selector(df, 'topPicks'),
        'grafica': get_chart(table),
        'historial':  allPicks(df).to_html(border=0, index=False),
    }

    return render(request, 'Picksbans.html', context)

# Función para generar la gráfica con los tops


def topPickBan(df: pd.DataFrame, type: str = 'picks') -> plt.Figure:
    if type == 'picks':
        df_filtered = df.filter(regex='^(BP|RP)[1-5]')
    elif type == 'bans':
        df_filtered = df.filter(regex='^(BB|RB)[1-5]')
    else:
        raise ValueError(f"{type} no es válido. Tiene que ser picks o bans")
    # Se cuenta cuántas veces se ha elegido cada personaje y lo guardamos en forma de porcentaje
    name_counts = df_filtered.stack().value_counts(normalize=True) * 100
    # Se obtiene el top 5
    top_champs = name_counts.head(5)
    # Se grafica el top 5 con una gráfica de barras horizontales
    fig, ax = plt.subplots(facecolor="#161616")
    # Se recorre el top 5 para obtener las imágenes de la API y se ponen a la izquierda de la gráfica
    for i, champ in enumerate(top_champs.keys()):
        # Se lee la imagen desde la URL
        url = f'{link}{champ}.png'
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        # Se crea el cuadro de imagen en la posición correspondiente
        imagebox = OffsetImage(img, zoom=0.25)
        ab = AnnotationBbox(imagebox, (0, i), xycoords='data', frameon=False)
        ax.add_artist(ab)
        # Se agrega el texto con el nombre y porcentaje del campeón al lado de la imagen
        ax.text(0.3, i, f'{champ} - {top_champs[champ]:.2f}%',
                ha='left', va='center', color='white', fontweight='bold')

    top_champs.plot.barh(ax=ax, color="#0059b3")

    # Se invierte el eje y para verlo de mayor a menor
    ax.invert_yaxis()
    ax.axis('off')

    return fig


def allPicks(df: pd.DataFrame) -> pd.DataFrame:
    df['Match'] = df['Blue'] + " - " + df['Red']
    df = df[['Split', 'Week', 'Match', 'Patch', 'BPPlayer1', 'BP1', 'BPPlayer2', 'BP2',
             'BPPlayer3', 'BP3', 'BPPlayer4', 'BP4', 'BPPlayer5', 'BP5', 'RPPlayer1', 'RP1', 'RPPlayer2', 'RP2',
             'RPPlayer3', 'RP3', 'RPPlayer4', 'RP4', 'RPPlayer5', 'RP5']]
    # Invertir el orden de las filas del DataFrame
    reversed_df = df.iloc[::-1].head(20)

    return reversed_df


def filterDF(request, season: str = year) -> render:
    if request.is_ajax() and request.method == 'POST':
        picks = pd.DataFrame(PicksBans.objects.filter(
            Match__Season=season).values())
        matchs = pd.DataFrame(Match.objects.filter(Season=season).values())
        df = pd.merge(picks, matchs, on='Match_id')

        # Obtener los valores de los campos del formulario
        team = request.POST.get('team-select')
        player = request.POST.get('player-select')
        split = request.POST.get('split-select')
        query = []
        filt = False

        if team:
            query.append(f"Blue == '{team}' | Red == '{team}'")
            filt = True
        if player:
            query.append(f"BPPlayer1 == '{player}' | BPPlayer2 == '{player}' | BPPlayer3 == '{player}' | BPPlayer4 == '{player}' | BPPlayer5 == '{player}' | RPPlayer1 == '{player}' | RPPlayer2 == '{player}' | RPPlayer3 == '{player}' | RPPlayer4 == '{player}' | RPPlayer5 == '{player}'")
            filt = True
        if split:
            query.append(f"Split == '{split}'")
            filt = True

        if filt:
            df_filt = df.query(" and ".join(query))
            table = topPickBan(df_filt)
        else:
            table = topPickBan(df)

        context = {
            'grafica': get_chart(table),
            'historial':  allPicks(df).to_html(border=0, index=False),
        }

        return JsonResponse(context)

# <!--Función para filtrar los datos leyendo el formulario-->
# def filterData():
#   team = js.document.getElementById('team-select').value
#   player = js.document.getElementById('player-select').value
#   split = js.document.getElementById('split-select').value
#   query = []
#   filt = False

#   if team != '':
#     query.append(f"Blue == '{team}' | Red == '{team}'")
#     filt = True
#   if player != '':
#     query.append(f"BPPlayer1 == '{player}' | BPPlayer2 == '{player}' | BPPlayer3 == '{player}' | BPPlayer4 == '{player}' | BPPlayer5 == '{player}' | RPPlayer1 == '{player}' | RPPlayer2 == '{player}' | RPPlayer3 == '{player}' | RPPlayer4 == '{player}' | RPPlayer5 == '{player}'")
#     filt = True
#   if split != '':
#     query.append(f"Split == '{split}'")
#     filt = True
#   if filt:
#     df_filt = df.query(" and ".join(query))
#     panel.object = topPickBan(df_filt)
#     panel2.object = allPicks(df_filt)


# def clearFilters():
#   #<!--Se guardan los valores de las etiquetas-->
#   team = js.document.getElementById('team-select').value
#   player = js.document.getElementById('player-select').value
#   split = js.document.getElementById('split-select').value
#   if not(team and player and split == ''):
#     #<!--Se establecen los valores de las etiquetas del formulario a vacio-->
#     js.document.getElementById('player-select').value = ''
#     js.document.getElementById('team-select').value = ''
#     js.document.getElementById('split-select').value = ''
#     #<!--Se vuelven a poner los valores iniciales-->
#     panel.object = topPickBan(df)
#     panel2.object = allPicks(df)


# def onChangingSelectedTeam():
# #<!--Se guardan los valores de las etiquetas-->
#   team = js.document.getElementById('team-select').value
#   if team:
#     df_filt = df.query(f"Blue == '{team}'").iloc[0].filter(regex='^(BPPlayer)[1-5]')
#     ps = '<option value=""></option>'
#     for row in df_filt:
#       ps = ps + '<option value="{}">{}</option>'.format(row,row)
#     js.document.getElementById('player-select').innerHTML = ps
#   else:
#     js.document.getElementById('player-select').innerHTML = players
