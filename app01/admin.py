from django.contrib import admin
from .models import EnglishWord
from .models import Academic
from .models import Testpaper
from .models import Record
admin.site.register(EnglishWord)
admin.site.register(Academic)
admin.site.register(Testpaper)
admin.site.register(Record)
# Register your models here.
