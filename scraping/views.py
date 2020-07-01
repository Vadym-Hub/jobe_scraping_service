from django.shortcuts import render

from .forms import FindForm
from .models import Vacancy


def home_view(request):
    """Пошук"""
    form = FindForm()
    return render(request, 'scraping/home.html', {'form': form})
