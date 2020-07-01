from django import forms

from scraping.models import City, Language, Vacancy


class FindForm(forms.Form):
    """Пошук по містам та спеціальностям із БД з вибором"""
    city = forms.ModelChoiceField(queryset=City.objects.all(), to_field_name="slug", required=False,
                                  widget=forms.Select(attrs={'class': 'form-control'}), label='Виберіть місто')
    language = forms.ModelChoiceField(queryset=Language.objects.all(), to_field_name="slug", required=False,
                                      widget=forms.Select(attrs={'class': 'form-control'}), label='Спеціальність')
