from django import forms
from django.forms import inlineformset_factory
from .models import CoilIn, CoilPallet, CoilNumber, SKU, CoilOut

class CoilInForm(forms.ModelForm):
    class Meta:
        model = CoilIn
        fields = ['timestamp1', 'user', 'lot', 'supplier', 'owner']
        widgets = {
             'timestamp1': forms.DateTimeInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50', 'type': 'datetime-local'}),
             'user': forms.Select(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'}),
             'lot': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'}),
             'supplier': forms.Select(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'}),
             'owner': forms.Select(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'}),
        }
        labels = {
            'timestamp1': 'วันที่/เวลา',
            'user': 'ผู้ใช้งาน',
            'lot': 'ล็อต',
            'supplier': 'ผู้จำหน่าย',
            'owner': 'เจ้าของ',
        }

class CoilPalletForm(forms.ModelForm):
    class Meta:
        model = CoilPallet
        fields = ['number', 'type0']
        widgets = {
            'number': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'}),
            'type0': forms.Select(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'}),
        }
        labels = {
            'number': 'หมายเลขพาเลท',
            'type0': 'ประเภทเหล็ก (SKU)',
        }

class CoilNumberForm(forms.ModelForm):
    class Meta:
        model = CoilNumber
        fields = ['number', 'weight']
        widgets = {
            'number': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'}),
            'weight': forms.NumberInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'}),
        }
        labels = {
            'number': 'หมายเลขม้วน',
            'weight': 'น้ำหนัก (กก.)',
        }

CoilNumberFormSet = inlineformset_factory(
    CoilPallet, CoilNumber, form=CoilNumberForm,
    fields=['number', 'weight'], extra=3, can_delete=True
)

class CoilOutForm(forms.ModelForm):
    class Meta:
        model = CoilOut
        fields = [
            'timestamp1', 'user', 'coil_number', 'sku',
            'full_coil_partial', 'coil_kg', 'type0',
            'job_number', 'job_name_short', 'job_qty',
            'department_cutting', 'note_1'
        ]
        widgets = {
            'timestamp1': forms.DateTimeInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50',
                'type': 'datetime-local'
            }),
            'user': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
            }),
            'coil_number': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
            }),
            'sku': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
            }),
            'full_coil_partial': forms.Select(choices=[
                ('', '---------'),
                ('เต็มม้วน', 'เต็มม้วน'),
                ('บางส่วน', 'บางส่วน'),
            ], attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
            }),
            'coil_kg': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50',
                'step': '0.01'
            }),
            'type0': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
            }),
            'job_number': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
            }),
            'job_name_short': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
            }),
            'job_qty': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
            }),
            'department_cutting': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
            }),
            'note_1': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
            }),
        }
        labels = {
            'timestamp1': 'วันที่/เวลา',
            'user': 'ผู้ใช้งาน',
            'coil_number': 'หมายเลขม้วน',
            'sku': 'SKU',
            'full_coil_partial': 'เต็มม้วน/บางส่วน',
            'coil_kg': 'น้ำหนัก (kg)',
            'type0': 'ประเภท',
            'job_number': 'เลขงาน',
            'job_name_short': 'ชื่องาน (ย่อ)',
            'job_qty': 'จำนวน',
            'department_cutting': 'แผนกที่ตัด',
            'note_1': 'หมายเหตุ',
        }
