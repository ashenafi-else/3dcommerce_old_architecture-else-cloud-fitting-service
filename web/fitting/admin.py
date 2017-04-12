from django.contrib import admin
from fitting.models import Scan, Shoe, User, Attribute, CompareResults

# Register your models here.
admin.site.register(Scan)
admin.site.register(Shoe)
admin.site.register(User)
admin.site.register(Attribute)
admin.site.register(CompareResults)
