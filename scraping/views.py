from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import ListView

from .forms import FindForm
from .models import Vacancy


def home_view(request):
    """Пошук"""
    form = FindForm()
    return render(request, 'scraping/home.html', {'form': form})


class VacancyListView(ListView):
    """Список вакансій"""
    model = Vacancy
    template_name = 'scraping/list.html'
    form = FindForm()
    paginate_by = 2

    def get_context_data(self, **kwargs):
        # Те, що ми перекидуєм в контекст
        context = super().get_context_data(**kwargs)
        context['city'] = self.request.GET.get('city')
        context['language'] = self.request.GET.get('language')
        context['form'] = self.form

        return context

    def get_queryset(self):
        city = self.request.GET.get('city')
        language = self.request.GET.get('language')
        qs = []
        if city or language:
            _filter = {}
            if city:
                _filter['city__slug'] = city
            if language:
                _filter['language__slug'] = language
            qs = Vacancy.objects.filter(**_filter).select_related('city', 'language')
        return qs
