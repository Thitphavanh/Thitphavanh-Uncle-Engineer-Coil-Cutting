from django.contrib import admin
from django.db import models as django_models
from django.contrib.admin import widgets
from .models import *

# Inlines
class CoilNumberInline(admin.TabularInline):
    model = CoilNumber
    extra = 1

class NWInline(admin.TabularInline):
    model = NW
    extra = 1

# Admins
class CoilPalletAdmin(admin.ModelAdmin):
    list_display = ['number', 'coilin', 'type0']
    inlines = [CoilNumberInline]

class LabelAdmin(admin.ModelAdmin):
    list_display = ['name', 'coilin', 'thickness', 'width', 'grade']
    inlines = [NWInline]

class CoilOutAdmin(admin.ModelAdmin):
    list_display = ['coil_number', 'sku', 'full_coil_partial', 'coil_kg', 'type0', 'job_number', 'job_name_short', 'job_qty', 'department_cutting', 'note_1']

    formfield_overrides = {
        django_models.DateTimeField: {'widget': widgets.AdminSplitDateTime},
    }

# Register your models here.
admin.site.register(Profile)
admin.site.register(Supplier)
admin.site.register(Owner)
admin.site.register(CoilIn)
admin.site.register(SKU)
admin.site.register(CoilPallet, CoilPalletAdmin)
admin.site.register(CoilNumber)
admin.site.register(Label, LabelAdmin)
admin.site.register(NW)
admin.site.register(CoilOut, CoilOutAdmin)
