from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    # Matchs
    path('matchs', matchHistory.matchs, name='matchs'),
    path('matchs/<int:season>', matchHistory.matchs, name='matchs'),
    path('matchs', matchHistory.onChangingSelectedWeek, name='onChangingSelectedWeek'),

    # Metrics
    path('metrics', metrics.metadata, name='metrics'),
    path('metrics/<int:season>', metrics.metadata, name='metrics'),

    # Heatmap
    path('heatmaps', heatmap.heatmaps, name='heatmaps'),
    
    # Top picks
    path('topPicks', topPicks.topPick, name='topPicks'),
    path('topPicks/<int:season>', topPicks.topPick, name='topPicks'),
    path('topPicks/', topPicks.filterDF, name='filtro'),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)