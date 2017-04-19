from django.contrib.admin import ModelAdmin


class BaseModelAdmin(ModelAdmin):
    readonly_fields_create = None

    def get_form(self, request, obj=None, **kwargs):
        form = super(BaseModelAdmin, self).get_form(request, **kwargs)
        form.request = request
        return form

    def get_readonly_fields(self, request, obj=None):
        if obj is None and self.readonly_fields_create is not None:
            return self.readonly_fields_create
        return self.readonly_fields
