from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
from LOLStatium_app.models import Positions
from .utils import *
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np

import requests
from PIL import Image
from io import BytesIO

def heatmaps(request, season=2023):
    """
    La función "heatmaps" genera un mapa de calor basado en datos de una base de datos y lo devuelve
    como parte de un contexto para representar una plantilla.

    :param request: El objeto de solicitud representa la solicitud HTTP que realizó el usuario para
    acceder a la página web. Contiene información como el navegador del usuario, la dirección IP y
    cualquier dato que se haya enviado con la solicitud
    :return: una plantilla HTML renderizada con las variables de contexto 'año', 'equipos', 'jugadores'
    y 'mapa'.
    """
    # Obtengo el dataframe a partir del modelo positions
    df = pd.DataFrame(Positions.objects.filter(Season=season).values())

    # Obtengo el mapa de calor
    heatmap = heatMapper(df, title='Kills Heatmap')

    # Creo el contexto de la vista
    context = {
        'year': season,
        'equipos': get_teams_selector(df),
        'jugadores': get_players_selector(df),
        'mapa': get_chart(heatmap),
    }

    return render(request, 'heatmap.html', context)


def transparent_cmap(cmap, N=255):
    mycmap = cmap
    mycmap._init()
    mycmap._lut[:, -1] = np.linspace(0, 1, N+4)
    return mycmap

# Método para generar el mapa de calor


def heatMapper(df: pd.DataFrame, type: str = 'Kill', title: str = 'Heatmap', ax=None):
    """
    La función `heatMapper` crea un mapa de calor usando un DataFrame de pandas y lo muestra en una
    figura de matplotlib.
    
    :param df: El marco de datos de entrada que contiene los datos para el mapa de calor
    :type df: pd.DataFrame
    :param type: El parámetro `type` se utiliza para filtrar los datos en el DataFrame. Especifica el
    tipo de datos que se utilizarán para crear el mapa de calor. En este caso, está configurado en
    "Matar", lo que significa que el mapa de calor se creará en función de los datos de muertes,
    defaults to Kill
    :type type: str (optional)
    :param title: El parámetro de título es una cadena que especifica el título del mapa de calor. Está
    configurado en 'Mapa de calor' de forma predeterminada, defaults to Heatmap
    :type title: str (optional)
    :param ax: El parámetro `ax` es un parámetro opcional que representa el objeto matplotlib Axes en el
    que se trazará el mapa de calor. Si no se proporciona ningún objeto "ax", se creará uno nuevo
    :return: un objeto de figura matplotlib.
    """
    df_heatmap = df[df['Type'] == type]
    # Se crea una figura de matplotlib con tamaño ajustado y color de la página
    fig = Figure(figsize=(4, 4), facecolor="#161616")
    ax = fig.add_subplot()
    # Se crea el gráfico hist2d en la figura
    img = plt.imread(BytesIO(requests.get("https://www.hotspawn.com/app/uploads/2020/03/summoners-rift.jpg").content),format="jpg")

    ax.imshow(img, extent=[0, 14820, 0, 14881])
    ax.hist2d(df_heatmap['X'], df_heatmap['Y'], bins=50,
              cmap=transparent_cmap(plt.cm.Reds))
    ax.set_xlim(0, 14820)
    ax.set_ylim(0, 14881)
    ax.set_aspect('equal')
    ax.axis('off')

    # Se devuelve la figura
    return ax.figure