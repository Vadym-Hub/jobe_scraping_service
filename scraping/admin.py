from django.contrib import admin

from scraping.models import City, Language


class CityAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}  # автоматичний slug


class LanguageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}  # автоматичний slug


admin.site.register(City, CityAdmin)
admin.site.register(Language, LanguageAdmin)
