
from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    if user.is_superuser:
        return True
    return user.groups.filter(name=group_name).exists()

@register.filter(name='is_sku_manager')
def is_sku_manager(user):
    if user.is_superuser:
        return True
    return user.groups.filter(name='SKU_Manager').exists()

@register.filter(name='is_coil_in')
def is_coil_in(user):
    if user.is_superuser:
        return True
    return user.groups.filter(name='Coil_In').exists()

@register.filter(name='is_coil_out')
def is_coil_out(user):
    if user.is_superuser:
        return True
    return user.groups.filter(name__in=['Coil_Out', 'Coil_In']).exists()

@register.filter(name='is_adjuster')
def is_adjuster(user):
    if user.is_superuser:
        return True
    return user.groups.filter(name='Adjuster').exists()

@register.filter(name='is_viewer')
def is_viewer(user):
    if user.is_superuser:
        return True
    return user.groups.filter(name__in=['Viewer', 'Coil_In', 'Coil_Out', 'Adjuster', 'SKU_Manager']).exists() or user.is_authenticated
