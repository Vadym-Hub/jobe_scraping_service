from django.urls import path
from scraping.views import home_view, VacancyListView

app_name = 'scraping'

urlpatterns = [
    path('', home_view, name='home'),
    path('list/', VacancyListView.as_view(), name='list'),
]
