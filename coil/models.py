from django.contrib.auth.models import User
import re
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username

class Supplier(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name or f"Supplier #{self.pk}"

class Owner(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name or f"Owner #{self.pk}"

class CoilIn(models.Model):
    timestamp1 = models.DateTimeField(null=True, blank=True)
    timestamp2 = models.DateField(auto_now=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    lot = models.CharField(max_length=255, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)


    def __str__(self):
        return self.lot or f"CoilIn #{self.pk}"

class SKU(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    Type0 = models.CharField(max_length=255, null=True, blank=True)
    Type1 = models.CharField(max_length=255, null=True, blank=True)
    Type2 = models.CharField(max_length=255, null=True, blank=True)
    thickness = models.CharField(max_length=255, null=True, blank=True,verbose_name='หนา')
    width = models.CharField(max_length=255, null=True, blank=True,verbose_name='กว้าง')
    length = models.CharField(max_length=255, null=True, blank=True,verbose_name='ยาว')
    color = models.CharField(max_length=255, null=True, blank=True)
    grade = models.CharField(max_length=255, null=True, blank=True)
    manufacturer = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    note1 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Note1 ขอบ กับ HRC')
    note2 = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        # Example format: เหล็กแผ่น ตปท-2T-1.6x89xC-FGY-85sk-D1-SE 4648
        
        # 1. Join dimensions
        dims = "x".join(filter(None, [str(self.thickness or '') if self.thickness else '', 
                                    str(self.width or '') if self.width else '', 
                                    str(self.length or '') if self.length else '']))
        
        # Clean color (strip Thai characters)
        color_val = str(self.color) if self.color else ''
        if color_val:
            color_val = re.sub(r'[\u0E00-\u0E7F]+', '', color_val)

        # 2. Collect dash-separated parts
        parts = []
        if self.name: parts.append(str(self.name))
        if self.Type0: parts.append(str(self.Type0))
        if self.Type1: parts.append(str(self.Type1))
        if self.Type2: parts.append(str(self.Type2))
        if dims: parts.append(dims)
        if color_val: parts.append(color_val)
        if self.grade: parts.append(str(self.grade))
        if self.note1: parts.append(str(self.note1))
        
        main_str = "-".join(parts)
        
        # 3. Add note2 with a space separator if it exists
        full_str = f"{main_str} {self.note2}" if self.note2 else main_str

        # Clean up any double dashes is still good practice
        cleaned_str = re.sub(r'-+', '-', full_str).strip('- ')

        return cleaned_str

class CoilPallet(models.Model):
    coilin = models.ForeignKey(CoilIn, on_delete=models.CASCADE)
    number = models.CharField(max_length=255, unique=True)
    type0 = models.ForeignKey(SKU, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.coilin} - Pallet {self.number}"


class CoilNumber(models.Model):
    coilpallet = models.ForeignKey(CoilPallet, on_delete=models.CASCADE)
    number = models.CharField(max_length=255, unique=True)
    weight = models.FloatField(null=True, blank=True)

    def __str__(self):
        # Format: Lot-PalletNumber-CoilNumber
        # e.g., K-25007-PL03(3)-C02
        try:
            return f"{self.coilpallet.coilin.lot}-{self.coilpallet.number}-{self.number}"
        except AttributeError:
            # Fallback if relationships are missing
            return self.number or f"Coil #{self.pk}"

class Label(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    coilin = models.ForeignKey(CoilIn, on_delete=models.CASCADE)
    thickness = models.CharField(max_length=255, null=True, blank=True)
    width = models.CharField(max_length=255, null=True, blank=True)
    grade = models.CharField(max_length=255, null=True, blank=True)
    color = models.CharField(max_length=255, null=True, blank=True)
    timestamp1 = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name or ""

@receiver(post_save, sender=CoilIn)
def create_label(sender, instance, created, **kwargs):
    if created:
        # Build the name: LOT-Supplier-Owner
        # Using 'or ""' to handle None values gracefully so we don't get "None" string
        lot = instance.lot or ""
        supplier = instance.supplier.name if instance.supplier else ""
        owner = instance.owner.name if instance.owner else ""
        
        name = f"{lot}-{supplier}-{owner}"
        
        Label.objects.create(
            name=name,
            coilin=instance
        )


class NW(models.Model):
    label = models.ForeignKey(Label, on_delete=models.CASCADE)
    nw_kg = models.FloatField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.label.name or f"NW #{self.pk}"


class CoilOut(models.Model):
    timestamp1 = models.DateTimeField(null=True, blank=True)
    timestamp2 = models.DateField(auto_now=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    coil_number = models.ForeignKey(CoilNumber, on_delete=models.CASCADE)
    sku = models.ForeignKey(SKU, on_delete=models.CASCADE)
    full_coil_partial = models.CharField(max_length=255, null=True, blank=True, verbose_name='เต็มม้วน/บางส่วน')
    coil_kg = models.FloatField(null=True, blank=True, verbose_name='Coil-Kg')
    type0 = models.CharField(max_length=255, null=True, blank=True)
    job_number = models.CharField(max_length=255, null=True, blank=True)
    job_name_short = models.CharField(max_length=255, null=True, blank=True)
    job_qty = models.CharField(max_length=255, null=True, blank=True)
    department_cutting = models.CharField(max_length=255, null=True, blank=True, verbose_name='แผนกที่ตัด')
    note_1 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Note-1')
   

    def __str__(self):
        return str(self.coil_number) if self.coil_number else f"CoilOut #{self.pk}"