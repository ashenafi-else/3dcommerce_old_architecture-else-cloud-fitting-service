from django.contrib import admin
from .models import Scan, Last, Product, User, Attribute, CompareResult, Size
from .proxy import ProductProxy, ProductAdmin


admin.site.site_title = 'Fitting'
admin.site.index_title = 'ELSE'
admin.site.site_header = 'ELSE Fitting Administration'

# Register your models here.
admin.site.register(ProductProxy, ProductAdmin)
admin.site.register(Scan)
admin.site.register(Last)
admin.site.register(Size)
admin.site.register(User)
admin.site.register(Attribute)
admin.site.register(CompareResult)
