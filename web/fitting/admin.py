from django.contrib import admin
from fitting.models import Scan, Shoe, User, Attribute, CompareResults


admin.site.site_title = 'Fitting'
admin.site.index_title = 'ELSE'
admin.site.site_header = 'ELSE Fitting Administration'

# Register your models here.
admin.site.register(Scan)
admin.site.register(Shoe)
admin.site.register(User)
admin.site.register(Attribute)
admin.site.register(CompareResults)
