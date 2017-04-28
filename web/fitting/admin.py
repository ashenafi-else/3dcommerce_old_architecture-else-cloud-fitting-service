from django.contrib import admin
from .models import Scan, Last, Product, User, ScanAttribute, CompareResult, Size
from .proxy import ProductProxy, ProductAdmin, LastProxy, LastAdmin,  ScanProxy, ScanAdmin


admin.site.site_title = 'Fitting'
admin.site.index_title = 'ELSE'
admin.site.site_header = 'ELSE Fitting Administration'

# Register your models here.
admin.site.register(ProductProxy, ProductAdmin)
admin.site.register(LastProxy, LastAdmin)
admin.site.register(ScanProxy, ScanAdmin)
admin.site.register(Size)
admin.site.register(User)
admin.site.register(CompareResult)
