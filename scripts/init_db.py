import os, django, sys
sys.path.append('LOLStatium_project')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LOLStatium_project.settings')

django.setup()

import Metadata
import PicksBans
import MatchHistory
import Positions
from db import db
from tqdm import tqdm

def main():
    """
    La función inserta marcos de datos de picks y bans, historial de partidos, metadatos
    y posiciones para una liga y temporada determinadas en una base de datos.
    """
    # Se instancia la liga y las temporadas
    league = input("Inserte una liga válida (LEC,LCS,LCK,LJL,PCS,VCS): ").upper()
    seasons = ['2020','2021','2022','2023']

    # Recorro la lista de los años, obtengo el dataframe de esa temporada
    # y la inserto en la BBDD
    for i in tqdm(range(len(seasons)), unit='MB'):
        # Picks y bans
        db.insertPicksBans(PicksBans.getDF_picksBans(
            league, seasons[i]))

        # # Historial de partida
        db.insertMatchHistory(MatchHistory.getDF_MH(league, seasons[i]))

        # Metadata
        db.insertMetaData(Metadata.getDF_metaData(league, seasons[i]))

        # Posiciones
        if seasons[i] == "2023":
            db.insertPositions(Positions.getDF_positions(league, seasons[i]))


if __name__ == "__main__":
    main()
