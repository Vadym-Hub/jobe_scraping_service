from django.contrib import admin

from scraping.models import City, Language, Vacancy, Error, Url


class CityAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}  # автоматичний slug


class LanguageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}  # автоматичний slug


admin.site.register(City, CityAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Vacancy)
admin.site.register(Error)
admin.site.register(Url)
