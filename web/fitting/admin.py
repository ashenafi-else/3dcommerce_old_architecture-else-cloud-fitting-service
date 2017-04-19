from django.contrib import admin
from fitting.models import Scan, Last, Product, User, Attribute, CompareResults, Shoe

# Register your models here.
admin.site.register(Scan)
admin.site.register(Shoe)
admin.site.register(Last)
admin.site.register(Product)
# admin.site.register(Sizes)
admin.site.register(User)
admin.site.register(Attribute)
admin.site.register(CompareResults)
