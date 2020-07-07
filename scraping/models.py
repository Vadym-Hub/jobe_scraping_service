import jsonfield  # Для цього потрібно поставити бібліотеку
from django.db import models


# Передача урлов для таблиці URL
def default_urls():
    return {"work": "", "rabota": "", "dou": "", "djinni": ""}


class City(models.Model):
    """Назва міста де шукаєм вакансію"""
    name = models.CharField(max_length=50, verbose_name='назва населеного пункту', unique=True)
    slug = models.SlugField(max_length=50, blank=True, unique=True)

    class Meta:
        verbose_name = 'назва населеного пункту'
        verbose_name_plural = 'назва населених пунктів'

    def __str__(self):
        return self.name


class Language(models.Model):
    """Мова програмування, для якої шукаєм вакансію"""
    name = models.CharField(max_length=50, verbose_name='мова програмування', unique=True)
    slug = models.SlugField(max_length=50, blank=True, unique=True)

    class Meta:
        verbose_name = 'мова програмування'
        verbose_name_plural = 'мови програмування'

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    """Збережені вакансії"""
    url = models.URLField(unique=True)
    title = models.CharField(max_length=250, verbose_name='заголовок вакансії')
    company = models.CharField(max_length=250, verbose_name='компанія')
    description = models.TextField(verbose_name='опис вакансії')
    city = models.ForeignKey('City', on_delete=models.CASCADE,
                             verbose_name='місто', related_name='vacancies')
    language = models.ForeignKey('Language', on_delete=models.CASCADE,
                                 verbose_name='мова програмування')
    timestamp = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'вакансія'
        verbose_name_plural = 'вакансії'
        ordering = ['-timestamp']

    def __str__(self):
        return self.title


class Error(models.Model):
    """Для помилок"""
    timestamp = models.DateField(auto_now_add=True)
    data = jsonfield.JSONField()

    def __str__(self):
        return str(self.timestamp)


class Url(models.Model):
    """Для збереження адресс для парсерів"""
    city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='місто')
    language = models.ForeignKey('Language', on_delete=models.CASCADE, verbose_name='мова програмування')
    url_data = jsonfield.JSONField(default=default_urls)

    class Meta:
        unique_together = ("city", "language")  # Для унікальності запису
