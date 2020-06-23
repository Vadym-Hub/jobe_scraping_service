from django.db import models


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
