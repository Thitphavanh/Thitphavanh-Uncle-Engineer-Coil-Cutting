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

import csv
import xlwt
from django.http import HttpResponse

def export_to_excel(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{modeladmin.model._meta.verbose_name_plural}.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Sheet1')

    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = [field.name for field in modeladmin.model._meta.fields]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    for obj in queryset:
        row_num += 1
        for col_num in range(len(columns)):
            val = getattr(obj, columns[col_num])
            if val is None:
                val = ""
            ws.write(row_num, col_num, str(val), font_style)

    wb.save(response)
    return response

export_to_excel.short_description = 'Export to Excel'

def export_to_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{modeladmin.model._meta.verbose_name_plural}.csv"'
    
    # Write BOM for Excel compatibility with UTF-8
    response.write(u'\ufeff'.encode('utf8'))

    writer = csv.writer(response)
    
    columns = [field.name for field in modeladmin.model._meta.fields]
    writer.writerow(columns) # Write header
    
    for obj in queryset:
        row = []
        for field in columns:
            val = getattr(obj, field)
            if val is None:
                val = ""
            row.append(str(val))
        writer.writerow(row)

    return response

export_to_csv.short_description = 'Export to CSV (Google Sheets)'

class SKUAdmin(admin.ModelAdmin):
    list_display = ['Type0', 'Type1', 'thickness', 'width', 'length', 'manufacturer', 'note1']
    actions = [export_to_excel, export_to_csv]

class CoilPalletAdmin(admin.ModelAdmin):
    list_display = ['number', 'coilin', 'type0']
    inlines = [CoilNumberInline]
    actions = [export_to_excel, export_to_csv]

class CoilNumberAdmin(admin.ModelAdmin):
    list_display = ['number', 'coilpallet', 'weight']
    actions = [export_to_excel, export_to_csv]

class LabelAdmin(admin.ModelAdmin):
    list_display = ['name', 'coilin', 'thickness', 'width', 'grade']
    inlines = [NWInline]

class CoilOutAdmin(admin.ModelAdmin):
    list_display = ['coil_number', 'sku', 'full_coil_partial', 'coil_kg', 'type0', 
                    'get_job_number', 'get_job_name_short', 'get_job_qty', 
                    'department_cutting', 'note_1']

    @admin.display(description='Job Number')
    def get_job_number(self, obj):
        return obj.job.job_number if obj.job else '-'

    @admin.display(description='Job Name Short')
    def get_job_name_short(self, obj):
        return obj.job.job_name_short if obj.job else '-'

    @admin.display(description='Job Qty')
    def get_job_qty(self, obj):
        return obj.job.job_qty if obj.job else '-'

    formfield_overrides = {
        django_models.DateTimeField: {'widget': widgets.AdminSplitDateTime},
    }

class JobAdmin(admin.ModelAdmin):
    list_display = ['job_number', 'job_name_short', 'job_qty', 'date_job']
    search_fields = ['job_number', 'job_name_short']

# Register your models here.
admin.site.register(Profile)
admin.site.register(Supplier)
admin.site.register(Owner)
admin.site.register(CoilIn)
admin.site.register(SKU, SKUAdmin)
admin.site.register(CoilPallet, CoilPalletAdmin)
admin.site.register(CoilNumber, CoilNumberAdmin)
admin.site.register(Label, LabelAdmin)
admin.site.register(NW)
admin.site.register(CoilOut, CoilOutAdmin)
admin.site.register(Job, JobAdmin)

