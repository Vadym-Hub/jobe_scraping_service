from django.urls import path
from scraping.views import VacancyListView, HomeView

app_name = 'scraping'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    #   path('', home_view, name='home'),
    path('list/', VacancyListView.as_view(), name='list'),
]
