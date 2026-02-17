from django import forms
from django.forms import inlineformset_factory
from .models import CoilIn, CoilPallet, CoilNumber, SKU, CoilOut, Job

class CoilInForm(forms.ModelForm):
    class Meta:
        model = CoilIn
        fields = ['timestamp1', 'lot', 'supplier', 'owner']
        widgets = {
             'timestamp1': forms.DateTimeInput(attrs={
                 'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50 datetimepicker',
                 'placeholder': 'YYYY-MM-DD HH:MM'
             }, format='%Y-%m-%d %H:%M'),
             'lot': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'}),
             'supplier': forms.Select(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'}),
             'owner': forms.Select(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'}),
        }
        labels = {
            'timestamp1': 'วันที่/เวลา',
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
    job_number = forms.ModelChoiceField(
        queryset=Job.objects.all(),
        label='เลขงาน',
        required=False,
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )
    job_name_short = forms.CharField(
        label='ชื่องาน (ย่อ)',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )
    job_qty = forms.CharField(
        label='จำนวน (ชิ้น)',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )

    class Meta:
        model = CoilOut
        fields = [
            'timestamp1', 'coil_number', 'sku',
            'full_coil_partial', 'coil_kg', 'type0',
            'department_cutting', 'note_1'
        ]
        widgets = {
            'timestamp1': forms.DateTimeInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50 datetimepicker',
                'placeholder': 'YYYY-MM-DD HH:MM'
            }, format='%Y-%m-%d %H:%M'),
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
            'department_cutting': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
            }),
            'note_1': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
            }),
        }
        labels = {
            'timestamp1': 'วันที่/เวลา',
            'coil_number': 'หมายเลขม้วน',
            'sku': 'SKU',
            'full_coil_partial': 'เต็มม้วน/บางส่วน',
            'coil_kg': 'น้ำหนัก (kg)',
            'type0': 'ประเภท',
            'department_cutting': 'แผนกที่ตัด',
            'note_1': 'หมายเหตุ',
        }

    def save(self, commit=True):
        instance = super(CoilOutForm, self).save(commit=False)
        # Use the selected Job instance directly
        instance.job = self.cleaned_data.get('job_number')
        if commit:
            instance.save()
        return instance

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = '__all__'
        widgets = {
            'date_job': forms.DateInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50',
                'type': 'date'
            }),
            'job_number': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'}),
            'job_name_short': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'}),
            'job_qty': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'}),
            # Add other fields as needed, keeping generic style for now
        }

class SKUForm(forms.ModelForm):
    class Meta:
        model = SKU
        fields = '__all__'
        widgets = {
            'Type0': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'}),
            'Type1': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'}),
            'Type2': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'}),
            'thickness': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'}),
            'width': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'}),
            'length': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'}),
            'color': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'}),
            'grade': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'}),
            'manufacturer': forms.Select(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'}),
            'note1': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'}),
            'note2': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'}),
        }
        labels = {
            'Type0': 'ประเภท 0',
            'Type1': 'ประเภท 1',
            'Type2': 'ประเภท 2',
            'thickness': 'ความหนา',
            'width': 'ความกว้าง',
            'length': 'ความยาว',
            'color': 'สี',
            'grade': 'เกรด',
            'manufacturer': 'ผู้ผลิต',
            'note1': 'หมายเหตุ 1',
            'note2': 'หมายเหตุ',
        }
