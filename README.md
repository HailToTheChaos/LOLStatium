# LOLStatium_Django
## 1 Introducción

Este proyecto consiste en crear una aplicación web con Django que muestra información y gráficos sobre el League of Legends a nivel competitivo.

El proyecto se centra en la liga LEC. 
Para obtener la información, se usa una técnica Web Scraping para extraer datos de otras páginas web. En este caso, se extraen los datos de la página lol.fandom.com, que los presenta en formato JSON. 
Los datos se transforman en un marco de datos para poder manejarlos y guardarlos en una base de datos. Tras su guardado, los datos se usan para crear las gráficas y estadísticas, que se muestran en la aplicación.

En la página web se muestran diferentes tipos de gráficos que ayudan a entender mejor el juego: mapas que indican dónde ocurren las acciones más importantes, barras que muestran los personajes más usados, tablas que comparan el rendimiento de los jugadores, etc. Estos gráficos se hacen con las librerias Matplotlib y Panel.

![Django](images/django.png)

## 2 Requisitos

- Python 3.11.4
- Django 4.2.4

### Instalación de dependencias
```bash
pip install -r requirements.txt
```

## 3 Uso
La aplicación ofrece las siguientes funcionalidades:

### Población de la base de datos

```bash
python scripts/init_db.py
```
## Créditos
- Autor: Jaime de la Fuente 