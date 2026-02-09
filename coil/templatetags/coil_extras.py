from django import template

register = template.Library()

def check_group(user, group_name):
    if user.is_superuser:
        return True
    return user.groups.filter(name=group_name).exists()

@register.filter(name='has_group') 
def has_group(user, group_name):
    return check_group(user, group_name)

@register.filter(name='is_sku_manager')
def is_sku_manager(user):
    return check_group(user, 'SKU_Manager')

@register.filter(name='is_coil_in')
def is_coil_in(user):
    return check_group(user, 'Coil_In')

@register.filter(name='is_coil_out')
def is_coil_out(user):
    return check_group(user, 'Coil_Out') or check_group(user, 'Coil_In')

@register.filter(name='is_adjuster')
def is_adjuster(user):
    return check_group(user, 'Adjuster')
